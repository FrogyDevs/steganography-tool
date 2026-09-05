import asyncio
from pathlib import Path

from stego_tool.app import StegoApp
from stego_tool.widgets.file_picker import FileSelected


async def _run_encode_flow_and_return_home(carrier: Path) -> None:
    app = StegoApp()
    async with app.run_test() as pilot:
        option_list = app.screen.query_one("OptionList")
        option_list.highlighted = 0  # "Encode"
        await pilot.press("enter")
        await pilot.pause()

        # FilePicker is on top; dismiss it the same way a real file click would.
        app.screen.dismiss(FileSelected(carrier))
        await pilot.pause()

        # MessageInput is on top; type a message and submit it.
        app.screen.query_one("Input").value = "secret"
        await pilot.press("enter")
        await pilot.pause()

        # The encode screen schedules a timer to pop itself and return to Home.
        # If that pop deadlocks the screen's own message pump, the app never
        # becomes idle again and pilot.pause() below hangs forever - so this
        # whole helper is wrapped in a hard timeout by the test itself.
        await asyncio.sleep(2.5)
        await pilot.pause()

        assert [type(screen).__name__ for screen in app.screen_stack] == [
            "Screen",
            "HomeScreen",
        ]

        option_list = app.screen.query_one("OptionList")
        assert option_list.highlighted == 0
        await pilot.press("down")
        await pilot.pause()
        assert option_list.highlighted == 1


def test_encode_screen_returns_to_interactive_home(tmp_path):
    carrier = tmp_path / "carrier.txt"
    carrier.write_text("hello world", encoding="utf-8")

    async def with_timeout():
        await asyncio.wait_for(_run_encode_flow_and_return_home(carrier), timeout=10)

    try:
        asyncio.run(with_timeout())
    except asyncio.TimeoutError:
        raise AssertionError(
            "App never became idle after EncodeScreen's return-to-Home timer fired - "
            "likely the screen's own timer deadlocked while popping itself. "
            "See EncodeScreen.on_message_entered's self.set_timer(...) call."
        )
