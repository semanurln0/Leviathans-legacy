import io
import unittest
from unittest.mock import patch, MagicMock
import pygame
from main import main, title_screen, play_level, GameState, connect_to_server
from OverviewUIHexagon import Button, TopBar, OverviewUI, Hexagon, Popup
from Buildings import BuildingFactory

class TestGameFunctions(unittest.TestCase):

    @patch('socket.socket.connect')
    def test_connect_to_server(self, mock_connect):
        # Test if connection is established successfully
        mock_socket = MagicMock(name='Socket')
        mock_connect.return_value = mock_socket
        client = connect_to_server()
        self.assertIsInstance(client, MagicMock)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('pygame.init')
    def test_title_screen(self, mock_pygame_init, mock_stdout):
        # Test if title screen returns GameState.MAIN_SCREEN when login button is clicked
        mock_pygame_init.return_value = None
        screen = MagicMock(name='Screen')
        game_state = GameState.TITLE
        self.assertEqual(title_screen(screen, game_state), GameState.MAIN_SCREEN)

    @patch('pygame.init')
    def test_play_level(self, mock_pygame_init):
        # Test if play level returns GameState.TITLE when return to main menu button is clicked
        mock_pygame_init.return_value = None
        screen = MagicMock(name='Screen')
        game_state = GameState.TITLE
        self.assertEqual(play_level(screen, game_state), GameState.TITLE)

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('builtins.input', side_effect=['testuser', 'testpass'])
    @patch('builtins.print')
    @patch('builtins.quit')
    @patch('pygame.init')
    def test_main(self, mock_pygame_init, mock_quit, mock_print, mock_input, mock_stdout):
        # Test if main function returns expected output
        mock_pygame_init.return_value = None
        main()
        mock_print.assert_called_with('login testuser testpass')
        mock_quit.assert_called()

class TestButton(unittest.TestCase):

    def setUp(self):
        self.screen = MagicMock(name='Screen')
        self.font = MagicMock(name='Font')
        self.button = Button("Test", pygame.Rect(0, 0, 100, 50), (255, 255, 255))
        self.button.font = self.font

    def test_is_clicked(self):
        # Test if is_clicked method returns True when mouse button is pressed inside the button's rect
        event = MagicMock(name='Event')
        event.type = pygame.MOUSEBUTTONDOWN
        event.pos = (50, 25)
        self.assertTrue(self.button.is_clicked(event))

    def test_is_not_clicked(self):
        # Test if is_clicked method returns False when mouse button is pressed outside the button's rect
        event = MagicMock(name='Event')
        event.type = pygame.MOUSEBUTTONDOWN
        event.pos = (150, 75)
        self.assertFalse(self.button.is_clicked(event))

    def test_draw(self):
        # Test if draw method correctly draws the button on the screen
        self.button.draw(self.screen)
        self.font.render.assert_called_once_with("Test", True, (255, 255, 255))
        self.screen.blit.assert_called_once()

class TestTopBar(unittest.TestCase):

    def setUp(self):
        self.screen = MagicMock(name='Screen')
        self.top_bar = TopBar(800)

    def test_add_button(self):
        # Test if add_button method correctly adds a button to the top bar
        button = MagicMock(name='Button')
        self.top_bar.add_button(button)
        self.assertIn(button, self.top_bar.buttons)

    def test_handle_events(self):
        # Test if handle_events method correctly handles events for each button in the top bar
        event = MagicMock(name='Event')
        button = MagicMock(name='Button')
        button.is_clicked.return_value = True
        self.top_bar.buttons.append(button)
        self.top_bar.handle_events([event])
        button.is_clicked.assert_called_once_with(event)

class TestOverviewUI(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.screen = MagicMock(name='Screen')
        self.ui = OverviewUI(self.screen, 'BackgroundPlaceHolder.png')

    @patch.object(OverviewUI, 'handle_game_events')
    def test_handle_events_hexagon_clicked(self, mock_handle_game_events):
        event = MagicMock(name='Event', type=pygame.MOUSEBUTTONDOWN)
        self.ui.popup.visible = False
        self.ui.handle_events([event])
        self.assertTrue(mock_handle_game_events.called)
        self.assertEqual(self.ui.popup.visible, True)

class TestHexagon(unittest.TestCase):

    def setUp(self):
        self.hexagon = Hexagon((100, 100), 50)

    def test_draw(self):
        # Test if draw method correctly draws the hexagon on the screen
        screen = MagicMock(name='Screen')
        self.hexagon.draw(screen)
        screen.draw.polygon.assert_called_once()

    def test_is_clicked(self):
        # Test if is_clicked method returns True when the hexagon is clicked
        event = MagicMock(name='Event')
        event.type = pygame.MOUSEBUTTONDOWN
        event.pos = (100, 100)
        self.assertTrue(self.hexagon.is_clicked(event))

    def test_is_not_clicked(self):
        # Test if is_clicked method returns False when the hexagon is not clicked
        event = MagicMock(name='Event')
        event.type = pygame.MOUSEBUTTONDOWN
        event.pos = (200, 200)
        self.assertFalse(self.hexagon.is_clicked(event))

class TestPopup(unittest.TestCase):

    def setUp(self):
        self.screen = MagicMock(name='Screen')
        self.rect = pygame.Rect(150, 100, 500, 400)
        self.popup = Popup(self.screen, self.rect)

    def test_draw(self):
        # Test if draw method correctly draws the popup on the screen
        self.popup.draw()
        self.assertTrue(self.screen.draw.rect.called)

    def test_handle_event_close(self):
        # Test if handle_event method closes the popup when close button is clicked
        event = MagicMock(name='Event')
        event.type = pygame.MOUSEBUTTONDOWN
        event.pos = (650, 100)
        self.assertTrue(self.popup.handle_event(event))
        self.assertFalse(self.popup.visible)

    def test_handle_event_upgrade(self):
        # Test if handle_event method upgrades the building when upgrade button is clicked
        event = MagicMock(name='Event')
        event.type = pygame.MOUSEBUTTONDOWN
        event.pos = (160, 130)
        self.popup.selected_hexagon = Hexagon((0, 0), 50)
        self.popup.selected_hexagon.building = MagicMock(name='Building')
        self.popup.selected_hexagon.building.upgrade_possible = True
        self.assertTrue(self.popup.handle_event(event))

    def test_handle_event_demolish(self):
        # Test if handle_event method demolishes the building when demolish button is clicked
        event = MagicMock(name='Event')
        event.type = pygame.MOUSEBUTTONDOWN
        event.pos = (270, 130)
        self.popup.selected_hexagon = Hexagon((0, 0), 50)
        self.popup.selected_hexagon.building = MagicMock(name='Building')
        self.assertTrue(self.popup.handle_event(event))

if __name__ == '__main__':
    unittest.main()
