import unittest
from unittest.mock import patch, MagicMock
import pygame
import random
from collections import namedtuple
import OverviewUI
import Player
from Buildings import (Buildings, Plantation, PowerPlant, Cabins, Barracks,
                       AbyssalOreRefinery, DefensiveDome, BuildingFactory)
from OverviewUIHexagon import Hexagon, Button, Popup, OverviewUI, TopBar
from UIElements import UIElement, TextBox, TextClickable, InputBox, InputBoxPass
from main import main, title_screen, play_level, GameState, LoginInfo
import test_game

Resolution = namedtuple('Resolution', ['width', 'height'])

SCREEN_RESOLUTIONS = {
    "1920x1080": Resolution(1920, 1080),
    "1366x768": Resolution(1366, 768),
    "1280x1024": Resolution(1280, 1024),
    "1440x900": Resolution(1440, 900),
    "1600x900": Resolution(1600, 900),
    "1680x1050": Resolution(1680, 1050),
    "1280x800": Resolution(1280, 800),
    "1024x768": Resolution(1024, 768),
    "2560x1440": Resolution(2560, 1440),
    "3840x2160": Resolution(3840, 2160)
}


class CustomRandomRetryRunner(unittest.TextTestRunner):
    MAX_RETRY_COUNT = 3

    def _makeResult(self):
        return CustomTextTestResult(self.stream, self.descriptions, self.verbosity)

    def run(self, test):
        result = super().run(test)
        if result.failures or result.errors:
            # If there are failures or errors, retry failed tests with random values
            for test_case, _ in result.failures + result.errors:
                retry_count = 0
                while retry_count < self.MAX_RETRY_COUNT:
                    # Generate random values and re-run the failed test
                    self._retry_test(test_case)
                    retry_count += 1
                    # Re-run the test suite
                    result = super().run(test)
                    # If the test passes, break the loop
                    if not result.failures and not result.errors:
                        break

    @staticmethod
    def _retry_test(test_case):
        # Iterate over all methods in the test case class
        for name in dir(test_case):
            if name.startswith("test_"):
                test_method = getattr(test_case, name)
                # Generate random values for parameters and re-run the test method
                test_method(random.randint(0, 100), random.choice(["a", "b", "c"]))


class CustomTextTestResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# Define a custom test runner for TestGameFunctions class
class CustomTestGameFunctionsRunner(unittest.TextTestRunner):
    def _makeResult(self):
        return CustomTextTestResult(self.stream, self.descriptions, self.verbosity)


# Define a custom test runner for TestTitleScreen class
class CustomTestTitleScreenRunner(unittest.TextTestRunner):
    def _makeResult(self):
        return CustomTextTestResult(self.stream, self.descriptions, self.verbosity)


# Define a custom test runner for TestPlayLevel class
class CustomTestPlayLevelRunner(unittest.TextTestRunner):
    def _makeResult(self):
        return CustomTextTestResult(self.stream, self.descriptions, self.verbosity)


# Define a custom test runner for TestHexagon class
class CustomTestHexagonRunner(unittest.TextTestRunner):
    def _makeResult(self):
        return CustomTextTestResult(self.stream, self.descriptions, self.verbosity)


# Define a custom test runner for TestButton class
class CustomTestButtonRunner(unittest.TextTestRunner):
    def _makeResult(self):
        return CustomTextTestResult(self.stream, self.descriptions, self.verbosity)


# Define a custom test runner for TestPopup class
class CustomTestPopupRunner(unittest.TextTestRunner):
    def _makeResult(self):
        return CustomTextTestResult(self.stream, self.descriptions, self.verbosity)


# Define a custom test runner for TestOverviewUI class
class CustomTestOverviewUIRunner(unittest.TextTestRunner):
    def _makeResult(self):
        return CustomTextTestResult(self.stream, self.descriptions, self.verbosity)


# Define a custom test runner for TestBuildings class
class CustomTestBuildingsRunner(unittest.TextTestRunner):
    def _makeResult(self):
        return CustomTextTestResult(self.stream, self.descriptions, self.verbosity)


# Define a custom test runner for TestPlayer class
class CustomTestPlayerRunner(unittest.TextTestRunner):
    def _makeResult(self):
        return CustomTextTestResult(self.stream, self.descriptions, self.verbosity)


# Define a custom test runner for TestUIElements class
class CustomTestUIElementsRunner(unittest.TextTestRunner):
    def _makeResult(self):
        return CustomTextTestResult(self.stream, self.descriptions, self.verbosity)


# Start test for main.py
class TestGameFunctions(unittest.TestCase):
    @patch('Player.connect_to_server')
    def test_main(self, mock_connect_to_server):
        mock_connect_to_server.return_value = MagicMock(name='ClientSocket')
        with patch('builtins.print') as mock_print:
            with patch('builtins.quit') as mock_quit:
                main()
                mock_print.assert_called_with('login testuser testpass')
                mock_quit.assert_called()


# Start test for TestTitleScreen class
class TestTitleScreen(unittest.TestCase):
    @patch('UIElements.TextBox')
    @patch('UIElements.UIElement')
    @patch('UIElements.InputBox')
    @patch('UIElements.InputBoxPass')
    def test_title_screen(self, mock_input_box_pass, mock_input_box, mock_ui_element, mock_text_box):
        screen = MagicMock(name='Screen')
        game_state = GameState.TITLE
        login = LoginInfo()
        login.set_login_info('testuser', 'testpass')
        with patch('main.inputs', return_value=GameState.MAIN_SCREEN):
            returned_state = title_screen(screen, game_state)
            self.assertEqual(returned_state, GameState.MAIN_SCREEN)
            mock_input_box.assert_called_with((screen.get_width() / 2) - 100, 350, 200, 36, "Enter your username")
            mock_input_box_pass.assert_called_with((screen.get_width() / 2) - 100, 400, 200, 36, "Enter your password")
            mock_ui_element.assert_any_call(center_position=(screen.get_width() / 2, 300), font_size=30, bg_rgb=None,
                                            text_rgb=(200, 200, 200), text="Login", action=GameState.MAIN_SCREEN)
            mock_ui_element.assert_any_call(center_position=(screen.get_width() / 2, 475), font_size=30, bg_rgb=None,
                                            text_rgb=(200, 200, 200), text="Quit", action=GameState.QUIT)
            mock_text_box.assert_called_with(center_position=(screen.get_width() / 2, 100), font_size=50,
                                             bg_rgb=None, text_rgb=(200, 200, 200), text="Leviathans legacy")


# Start test for TestPlayLevel class
class TestPlayLevel(unittest.TestCase):
    def test_play_level(self):
        screen = MagicMock(name='Screen')
        game_state = GameState.TITLE
        with patch('main.inputs', return_value=GameState.TITLE):
            returned_state = play_level(screen, game_state)
            self.assertEqual(returned_state, GameState.TITLE)


# Start test for TestHexagon class
class TestHexagon(unittest.TestCase):
    def test_hexagon_init(self):
        hexagon = Hexagon((100, 100), 30)
        self.assertEqual(hexagon.center, (100, 100))
        self.assertEqual(hexagon.size, 30)
        self.assertEqual(hexagon.color, (100, 100, 100))
        self.assertEqual(hexagon.id, 0)  # Assuming global variable initialization starts from 0

    def test_hexagon_draw(self):
        screen_mock = MagicMock(name='Screen')
        hexagon = Hexagon((100, 100), 30)
        hexagon.draw(screen_mock)
        screen_mock.assert_called_once_with((200, 100), (100, 100), 30)


# Start test for TestButton class
class TestButton(unittest.TestCase):
    def test_button_init(self):
        button = Button("Test Button", pygame.Rect(100, 100, 200, 50), (255, 0, 0))
        self.assertEqual(button.label, "Test Button")
        self.assertEqual(button.rect, pygame.Rect(100, 100, 200, 50))
        self.assertEqual(button.color, (255, 0, 0))


# Start test for TestPopup class
class TestPopup(unittest.TestCase):
    def test_popup_init(self):
        screen_mock = MagicMock(name='Screen')
        popup = Popup(screen_mock, pygame.Rect(100, 100, 200, 200))
        self.assertEqual(popup.screen, screen_mock)
        self.assertEqual(popup.rect, pygame.Rect(100, 100, 200, 200))
        self.assertFalse(popup.visible)


# Start test for TestOverviewUI class
class TestOverviewUI(unittest.TestCase):
    @patch('pygame.display.set_mode', side_effect=test_game.mock_display_set_mode)
    @patch('pygame.display.flip', side_effect=test_game.mock_display_flip)
    @patch('pygame.quit', side_effect=test_game.mock_pygame_quit)
    def test_overview_ui_init(self, _):
        mplayer_mock = test_game.MockPlayer()
        ui = OverviewUI(None, None, mplayer_mock)
        self.assertIsInstance(ui.screen, MagicMock)
        self.assertIsInstance(ui.top_bar, TopBar)
        self.assertIsInstance(ui.popup, Popup)
        # Add more assertions as needed

    def test_overview_ui_initialize_buttons(self):
        screen_mock = MagicMock(name='Screen')
        ui = OverviewUI(screen_mock, None, None)
        ui.initialize_buttons()
        self.assertEqual(len(ui.top_bar.buttons), 6)
        # Add more assertions as needed


# Start test for TestBuildings class
class TestBuildings(unittest.TestCase):
    def setUp(self):
        self.building = Buildings()

    def test_building_init(self):
        self.assertEqual(self.building.build_cost, 10)
        self.assertEqual(self.building.build_time, 1)
        self.assertTrue(self.building.upgrade_possible)
        self.assertTrue(self.building.buyable)
        self.assertEqual(self.building.building_stage, 0)
        self.assertEqual(self.building.increase_rate_of_price, 1)
        self.assertEqual(self.building.increase_rate_of_build_time, 1.5)
        self.assertEqual(self.building.base_image_path, "sprites")
        self.assertEqual(self.building.image_filename, "SimpleBuilding.png")
        self.assertIsInstance(self.building.image, MagicMock)
        self.assertIsNone(self.building.upgrade_end_time)

    # Add more tests for Buildings class methods if needed


class TestPlantation(unittest.TestCase):

    def setUp(self):
        self.plantation = Plantation()

    def test_plantation_init(self):
        self.assertEqual(self.plantation.build_cost, 20)
        self.assertEqual(self.plantation.build_time, 30)
        self.assertEqual(self.plantation.production_rate, 5)

    # Add more tests for Plantation class methods if needed


class TestPowerPlant(unittest.TestCase):

    def setUp(self):
        self.powerplant = PowerPlant()

    def test_powerplant_init(self):
        self.assertEqual(self.powerplant.build_cost, 40)
        self.assertEqual(self.powerplant.build_time, 45)
        self.assertEqual(self.powerplant.energy_output, 100)

    # Add more tests for PowerPlant class methods if needed


class TestCabins(unittest.TestCase):

    def setUp(self):
        self.cabins = Cabins()

    def test_cabins_init(self):
        self.assertEqual(self.cabins.build_cost, 30)
        self.assertEqual(self.cabins.build_time, 20)

    # Add more tests for Cabins class methods if needed


class TestBarracks(unittest.TestCase):

    def setUp(self):
        self.barracks = Barracks()

    def test_barracks_init(self):
        self.assertEqual(self.barracks.build_cost, 50)
        self.assertEqual(self.barracks.build_time, 60)

    # Add more tests for Barracks class methods if needed


class TestAbyssalOreRefinery(unittest.TestCase):

    def setUp(self):
        self.refinery = AbyssalOreRefinery()

    def test_refinery_init(self):
        self.assertEqual(self.refinery.build_cost, 70)
        self.assertEqual(self.refinery.build_time, 80)
        self.assertEqual(self.refinery.ore_processing_rate, 15)

    # Add more tests for AbyssalOreRefinery class methods if needed


class TestDefensiveDome(unittest.TestCase):

    def setUp(self):
        self.dome = DefensiveDome()

    def test_dome_init(self):
        self.assertEqual(self.dome.build_cost, 100)
        self.assertEqual(self.dome.build_time, 90)
        self.assertEqual(self.dome.defense_capability, 200)

    # Add more tests for DefensiveDome class methods if needed


class TestBuildingFactory(unittest.TestCase):

    def setUp(self):
        self.factory = BuildingFactory()

    def test_create_building(self):
        building_types = ['plantation', 'powerplant', 'cabins', 'barracks', 'abyssalorerefinery', 'defensivedome']
        for building_type in building_types:
            building = self.factory.create_building(building_type)
            self.assertIsNotNone(building)
            self.assertIsInstance(building, Buildings)

    def test_create_unknown_building(self):
        with self.assertRaises(ValueError):
            self.factory.create_building('unknown_type')


# Start test for TestPlayer class
class TestPlayer(unittest.TestCase):
    @patch('Player.socket.socket')
    def test_get_player_info(self, mock_socket):
        # Prepare mock objects
        mock_client = MagicMock()
        mock_socket.return_value = mock_client
        mock_client.recv.return_value = "10000 10000 0"
        player = Player.Player(client=mock_client)

        # Call the function
        result = player.get_player_info()

        # Assertions
        self.assertEqual(result, ["10000", "10000", "0"])
        mock_client.send.assert_called_once()
        mock_client.recv.assert_called_once()

    @patch('Player.socket.socket')
    def test_get_buildings(self, mock_socket):
        # Prepare mock objects
        mock_client = MagicMock()
        mock_socket.return_value = mock_client
        mock_client.recv.return_value = "(1, 1, 'plantation', 1)^^(1, 2, 'cabins', 1)"
        player = Player.Player(client=mock_client)

        # Call the function
        result = player.get_buildings()

        # Assertions
        self.assertEqual(result, ["(1, 1, 'plantation', 1)", "(1, 2, 'cabins', 1)"])
        mock_client.send.assert_called_once()
        mock_client.recv.assert_called_once()

    @patch('Player.socket.socket')
    def test_commit_building(self, mock_socket):
        # Prepare mock objects
        mock_client = MagicMock()
        mock_socket.return_value = mock_client
        player = Player.Player(client=mock_client)

        # Call the function
        player.commit_building(1, 1, 1)

        # Assertions
        mock_client.send.assert_called_once_with(b'add_building 1 1 1')
        mock_client.recv.assert_not_called()


# Start test for TestUIElements class
class TestUIElements(unittest.TestCase):
    def setUp(self):
        pygame.init()

    def tearDown(self):
        pygame.quit()

    def test_UIElement(self):
        # Create a mock action function
        def action_func():
            return "Action performed"

        # Create a UIElement instance
        ui_element = UIElement((100, 100), "Button", 20, (0, 0, 0), (255, 255, 255), action=action_func)

        # Test default properties
        self.assertFalse(ui_element.mouse_over)
        self.assertEqual(ui_element.image.get_size(), (16, 20))
        self.assertEqual(ui_element.rect.size, (16, 20))
        self.assertIsNone(ui_element.action)

        # Test update method
        self.assertIsNone(ui_element.update((100, 100), True, None))
        self.assertTrue(ui_element.mouse_over)

        # Test draw method
        surface = pygame.Surface((200, 200))
        ui_element.draw(surface)

    def test_TextBox(self):
        # Create a TextBox instance
        text_box = TextBox((100, 100), "Text", 20, (0, 0, 0), (255, 255, 255))

        # Test default properties
        self.assertEqual(text_box.image.get_size(), (32, 20))
        self.assertEqual(text_box.rect.size, (32, 20))

        # Test draw method
        surface = pygame.Surface((200, 200))
        text_box.draw(surface)

    def test_TextClickable(self):
        # Create a TextClickable instance
        text_clickable = TextClickable((100, 100), "Click Me", 20, (0, 0, 0), (255, 255, 255))

        # Test default properties
        self.assertFalse(text_clickable.mouse_over)
        self.assertEqual(text_clickable.image.get_size(), (64, 20))
        self.assertEqual(text_clickable.rect.size, (64, 20))

        # Test update method
        self.assertIsNone(text_clickable.update((100, 100), True, None))
        self.assertTrue(text_clickable.mouse_over)

        # Test draw method
        surface = pygame.Surface((200, 200))
        text_clickable.draw(surface)

    def test_InputBox(self):
        # Create an InputBox instance
        input_box = InputBox(50, 50, 100, 20)

        # Test default properties
        self.assertEqual(input_box.color, "White")
        self.assertEqual(input_box.txt_color, "White")
        self.assertEqual(input_box.bg_color, (26, 79, 101, 200))
        self.assertEqual(input_box.text, "")
        self.assertEqual(input_box.font_size, 16)
        self.assertFalse(input_box.active)
        self.assertEqual(input_box.rect.size, (100, 20))

        # Test handle_event method
        input_box.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(60, 60)))
        self.assertTrue(input_box.active)
        input_box.handle_event(pygame.event.Event(pygame.KEYDOWN, unicode="A"))
        self.assertEqual(input_box.text, "A")

        # Test draw method
        surface = pygame.Surface((200, 200))
        input_box.draw(surface)

    def test_InputBoxPass(self):
        # Create an InputBoxPass instance
        input_box_pass = InputBoxPass(50, 50, 100, 20)

        # Test default properties
        self.assertEqual(input_box_pass.color, "White")
        self.assertEqual(input_box_pass.txt_color, "White")
        self.assertEqual(input_box_pass.text, "")
        self.assertEqual(input_box_pass.font_size, 16)
        self.assertFalse(input_box_pass.active)
        self.assertEqual(input_box_pass.rect.size, (100, 20))

        # Test handle_event method
        input_box_pass.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(60, 60)))
        self.assertTrue(input_box_pass.active)
        input_box_pass.handle_event(pygame.event.Event(pygame.KEYDOWN, unicode="A"))
        self.assertEqual(input_box_pass.text, "*")

        # Test text_return method
        self.assertEqual(input_box_pass.text_return(), "A")

        # Test draw method
        surface = pygame.Surface((200, 200))
        input_box_pass.draw(surface)


# Start test for OverviewUI.py
class TestOverviewUILoginScreen(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.Surface((800, 600))
        # Choose a random resolution from the available options
        resolution_key = random.choice(list(SCREEN_RESOLUTIONS.keys()))
        resolution = SCREEN_RESOLUTIONS[resolution_key]
        self.screen = MagicMock(name='Screen', return_value=pygame.Surface((resolution.width, resolution.height)))
        self.ui = OverviewUI.OverviewUI(self.screen, 'BackgroundPlaceHolder.png')

    def test_button_click(self):
        # Simulate button click event
        button = self.ui.top_bar.buttons[0]
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(button.rect.centerx, button.rect.centery))
        self.ui.handle_events([event])
        self.assertTrue(button.is_clicked(event))

    def test_building_slot_click(self):
        # Simulate building slot click event
        slot = self.ui.building_slots[0]
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(slot['rect'].centerx, slot['rect'].centery))
        self.ui.handle_events([event])
        self.assertTrue(slot['clicked'])

    def test_draw(self):
        # Ensure draw function doesn't throw any errors
        self.ui.draw()

    def tearDown(self):
        pygame.quit()


if __name__ == '__main__':
    # Create test suite for each class
    suite_game_functions = unittest.TestLoader().loadTestsFromTestCase(TestGameFunctions)
    suite_title_screen = unittest.TestLoader().loadTestsFromTestCase(TestTitleScreen)
    suite_play_level = unittest.TestLoader().loadTestsFromTestCase(TestPlayLevel)
    suite_hexagon = unittest.TestLoader().loadTestsFromTestCase(TestHexagon)
    suite_button = unittest.TestLoader().loadTestsFromTestCase(TestButton)
    suite_popup = unittest.TestLoader().loadTestsFromTestCase(TestPopup)
    suite_overview_ui = unittest.TestLoader().loadTestsFromTestCase(TestOverviewUI)
    suite_buildings = unittest.TestLoader().loadTestsFromTestCase(TestBuildings)
    suite_player = unittest.TestLoader().loadTestsFromTestCase(TestPlayer)
    suite_ui_elements = unittest.TestLoader().loadTestsFromTestCase(TestUIElements)
    suite_overview_ui_login_screen = unittest.TestLoader().loadTestsFromTestCase(TestOverviewUILoginScreen)

    # Run each test suite using custom test runners
    CustomRandomRetryRunner().run(suite_game_functions)
    CustomRandomRetryRunner().run(suite_title_screen)
    CustomRandomRetryRunner().run(suite_play_level)
    CustomRandomRetryRunner().run(suite_hexagon)
    CustomRandomRetryRunner().run(suite_button)
    CustomRandomRetryRunner().run(suite_popup)
    CustomRandomRetryRunner().run(suite_overview_ui)
    CustomRandomRetryRunner().run(suite_buildings)
    CustomRandomRetryRunner().run(suite_player)
    CustomRandomRetryRunner().run(suite_ui_elements)
    CustomRandomRetryRunner().run(suite_overview_ui_login_screen)
