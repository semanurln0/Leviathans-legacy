import unittest
from unittest.mock import patch, MagicMock
import pygame
from main import main, title_screen, play_level, GameState
from OverviewUIHexagon import Button, TopBar, OverviewUI, Hexagon, Popup
from Buildings import BuildingFactory, Buildings, time
from Server import server
from Player import Player, connect_to_server
from UIElements import create_surface_with_text, BLUE, WHITE, InputBox, InputBoxPass

# start test for main.py
class TestGameFunctions(unittest.TestCase):

    @patch('socket.socket.connect')
    def test_connect_to_server(self, mock_connect):
        # Test if connection is established successfully
        mock_socket = MagicMock(name='Socket')
        mock_connect.return_value = mock_socket
        client = connect_to_server()
        self.assertIsInstance(client, MagicMock)

    @patch('pygame.init')
    def test_title_screen(self, mock_pygame_init):
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

    @patch('builtins.print')
    @patch('builtins.quit')
    @patch('pygame.init')
    def test_main(self, mock_pygame_init, mock_quit, mock_print):
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


# start test for OverviewUIHexagon.py
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


# start test for Buildings.py
class TestBuildingFactory(unittest.TestCase):
    def test_create_building(self):
        factory = BuildingFactory()
        building_types = ['plantation', 'power_plant', 'cabins', 'barracks', 'abyssal_ore_refinery', 'defensive_dome']
        for building_type in building_types:
            building = factory.create_building(building_type)
            self.assertIsInstance(building, Buildings)

    def test_create_unknown_building(self):
        factory = BuildingFactory()
        with self.assertRaises(ValueError):
            factory.create_building('unknown_building')


class TestBuildings(unittest.TestCase):
    @patch('time.time')
    def test_upgrade(self, mock_time):
        building = Buildings()
        # Ensure upgrade_possible and enough steel for upgrade
        building.upgrade_possible = True
        building.build_cost = 10
        building.building_stage = 1
        building.steel = 20
        building.upgrade_end_time = None

        building.upgrade()
        self.assertEqual(building.steel, 10)  # Check steel deducted
        self.assertEqual(building.building_stage, 2)  # Check building stage increased

        # Ensure upgrade not possible when already upgrading
        building.upgrade_end_time = time.time() + 10
        building.upgrade()
        self.assertEqual(building.steel, 10)  # Check steel not further deducted
        self.assertEqual(building.building_stage, 2)  # Check building stage not increased

        # Ensure upgrade not possible when not enough steel
        building.steel = 5
        building.upgrade_end_time = None
        building.upgrade()
        self.assertEqual(building.steel, 5)  # Check steel not deducted
        self.assertEqual(building.building_stage, 2)  # Check building stage not increased

    def test_demolish(self):
        building = Buildings()
        building.building_stage = 2
        building.demolish()
        self.assertEqual(building.building_stage, 1)  # Check building stage decreased

        building.building_stage = 0  # Ensure stage cannot be negative
        building.demolish()
        self.assertEqual(building.building_stage, 0)  # Check building stage remains 0


# start test for server.py
class TestServerFunctions(unittest.TestCase):

    @patch('socket.socket')
    def test_handle_client_login_accepted(self, mock_socket):
        # Mock client socket and address
        client_socket = MagicMock(name='ClientSocket')
        addr = ("127.0.0.1", 12345)
        mock_socket.return_value.accept.return_value = (client_socket, addr)

        # Mock database query result for login request
        querier = MagicMock(name='Querier')
        querier.fetchone.return_value = (1, "testuser", "testpass", "other_data")
        connection = MagicMock(name='Connection')
        connection.cursor.return_value = querier
        server.connect_db = MagicMock(return_value=connection)

        # Simulate login request from client
        client_socket.recv.return_value = "login testuser testpass".encode("utf-8")
        server.handle_client(client_socket, addr)

        # Assert that the server responds with "accepted"
        client_socket.send.assert_called_with("accepted".encode("utf-8"))

    # Assuming the previous test case for login is already included here

    @patch('socket.socket')
    def test_handle_client_info(self, mock_socket):
        # Mock client socket and address
        client_socket = MagicMock(name='ClientSocket')
        addr = ("127.0.0.1", 12345)
        mock_socket.return_value.accept.return_value = (client_socket, addr)

        # Mock database query result for "info" request
        querier = MagicMock(name='Querier')
        querier.fetchone.return_value = (1, "testuser", "other_data")
        connection = MagicMock(name='Connection')
        connection.cursor.return_value = querier
        server.connect_db = MagicMock(return_value=connection)

        # Simulate "info" request from client
        client_socket.recv.return_value = "info".encode("utf-8")
        server.handle_client(client_socket, addr)

        # Assert that the server responds with player information
        expected_response = "other_data"
        client_socket.send.assert_called_with(expected_response.encode("utf-8"))

    @patch('socket.socket')
    def test_handle_client_info_buildings(self, mock_socket):
        # Mock client socket and address
        client_socket = MagicMock(name='ClientSocket')
        addr = ("127.0.0.1", 12345)
        mock_socket.return_value.accept.return_value = (client_socket, addr)

        # Mock database query result for "info_buildings" request
        querier = MagicMock(name='Querier')
        querier.fetchall.return_value = [(1, "building1"), (2, "building2")]
        connection = MagicMock(name='Connection')
        connection.cursor.return_value = querier
        server.connect_db = MagicMock(return_value=connection)

        # Simulate "info_buildings" request from client
        client_socket.recv.return_value = "info_buildings".encode("utf-8")
        server.handle_client(client_socket, addr)

        # Assert that the server responds with building information
        expected_response = "[(1, 'building1')] [(2, 'building2')] "
        client_socket.send.assert_called_with(expected_response.encode("utf-8"))

# start test for Player.py
class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player()
        self.client = MagicMock(name='ClientSocket')

    @patch('Player.connect_to_server')
    def test_get_player_info(self, mock_connect_to_server):
        # Mock connect_to_server to return a mocked client
        mock_connect_to_server.return_value = self.client

        # Mock recv method of the client to return player info
        self.client.recv.return_value = "10000 10000 0".encode("utf-8")

        # Call get_player_info method
        info = self.player.get_player_info()

        # Assert that the client sent the "info" request
        self.client.send.assert_called_with("info".encode("utf-8")[:1024])

        # Assert that the player info is correctly received and processed
        self.assertEqual(info, ["10000", "10000", "0"])

    @patch('Player.connect_to_server')
    def test_get_buildings(self, mock_connect_to_server):
        # Mock connect_to_server to return a mocked client
        mock_connect_to_server.return_value = self.client

        # Mock recv method of the client to return building info
        self.client.recv.return_value = "building1 building2".encode("utf-8")

        # Call get_buildings method
        self.player.get_buildings()

        # Assert that the client sent the "info_buildings" request
        self.client.send.assert_called_with("info_buildings".encode("utf-8")[:1024])

# start test for UIElements.py
class TestInputBox(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.input_box = InputBox(100, 100, 200, 50)

    def test_handle_event(self):
        event = MagicMock()
        event.type = pygame.MOUSEBUTTONDOWN
        event.pos = (110, 110)
        self.input_box.handle_event(event)
        self.assertTrue(self.input_box.active)

    def test_update(self):
        self.input_box.text = "Test Text"
        self.input_box.update()
        self.assertEqual(self.input_box.txt_surface.get_text(), "Test Text")

    def test_text_return(self):
        self.input_box.text = "Test Text"
        self.assertEqual(self.input_box.text_return(), "Test Text")

    def tearDown(self):
        pygame.quit()

class TestInputBoxPass(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.input_box_pass = InputBoxPass(100, 100, 200, 50)

    def test_handle_event(self):
        event = MagicMock()
        event.type = pygame.MOUSEBUTTONDOWN
        event.pos = (110, 110)
        self.input_box_pass.handle_event(event)
        self.assertTrue(self.input_box_pass.active)

    def test_update(self):
        self.input_box_pass.text = "Test Text"
        self.input_box_pass.update()
        self.assertEqual(self.input_box_pass.txt_surface.get_text(), "Test Text")

    def test_text_return(self):
        self.input_box_pass.text = "Test Text"
        self.assertEqual(self.input_box_pass.text_return(), "Test Text")

    def tearDown(self):
        pygame.quit()


if __name__ == '__main__':
    unittest.main()
