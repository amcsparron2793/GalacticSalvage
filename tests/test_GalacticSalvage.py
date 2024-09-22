import unittest
from unittest.mock import Mock, patch, ANY

from GalacticSalvage.GalacticSalvage import GalacticSalvage


class GalacticSalvageTest(unittest.TestCase):
    def setUp(self):
        self.gs = GalacticSalvage()

    def test_check_keydown_events(self):
        mock_event = Mock()
        with patch.object(self.gs, '_check_keydown_events') as mock_method:
            self.gs._check_keydown_events(mock_event)
            mock_method.assert_called_with(mock_event)

    def test_check_keyup_events(self):
        mock_event = Mock()
        with patch.object(self.gs, '_check_keyup_events') as mock_method:
            self.gs._check_keyup_events(mock_event)
            mock_method.assert_called_with(mock_event)

    def test_check_play_button(self):
        mock_pos = Mock()
        with patch.object(self.gs, '_check_play_button') as mock_method:
            self.gs._check_play_button(mock_pos)
            mock_method.assert_called_with(mock_pos)

    def test_fire_bullet(self):
        with patch.object(self.gs, '_fire_bullet') as mock_method:
            self.gs._fire_bullet()
            mock_method.assert_called_with()

    def test_update_bullets(self):
        with patch.object(self.gs, '_update_bullets') as mock_method:
            self.gs._update_bullets()
            mock_method.assert_called_with()

    def test_check_bullet_asteroid_collisions(self):
        with patch.object(self.gs, '_check_bullet_asteroid_collisions') as mock_method:
            self.gs._check_bullet_asteroid_collisions()
            mock_method.assert_called_with()

    def test_check_asteroid_ship_collisions(self):
        with patch.object(self.gs, '_check_asteroid_ship_collisions') as mock_method:
            self.gs._check_asteroid_ship_collisions()
            mock_method.assert_called_with()

    def test_check_broken_ship_ship_collisions(self):
        with patch.object(self.gs, '_check_broken_ship_ship_collisions') as mock_method:
            self.gs._check_broken_ship_ship_collisions()
            mock_method.assert_called_with()

    def test_check_extra_life_ship_collisions(self):
        with patch.object(self.gs, '_check_extra_life_ship_collisions') as mock_method:
            self.gs._check_extra_life_ship_collisions()
            mock_method.assert_called_with()

    def test_create_asteroids(self):
        with patch.object(self.gs, '_create_asteroids') as mock_method:
            self.gs._create_asteroids()
            mock_method.assert_called_with()

    def test_update_asteroids(self):
        with patch.object(self.gs, '_update_asteroids') as mock_method:
            self.gs._update_asteroids()
            mock_method.assert_called_with()

    def test_create_broken_ship(self):
        with patch.object(self.gs, '_create_broken_ship') as mock_method:
            self.gs._create_broken_ship()
            mock_method.assert_called_with()

    def test_update_broken_ship(self):
        with patch.object(self.gs, '_update_broken_ship') as mock_method:
            self.gs._update_broken_ship()
            mock_method.assert_called_with()

    def test_create_extra_life(self):
        with patch.object(self.gs, '_create_extra_life') as mock_method:
            self.gs._create_extra_life()
            mock_method.assert_called_with()

    def test_update_extra_life(self):
        with patch.object(self.gs, '_update_extra_life') as mock_method:
            self.gs._update_extra_life()
            mock_method.assert_called_with()

    def test_UpdateStars(self):
        with patch.object(self.gs, '_UpdateStars') as mock_method:
            self.gs._UpdateStars()
            mock_method.assert_called_with()

    def test_check_system_events(self):
        with patch.object(self.gs, '_check_system_events') as mock_method:
            self.gs._check_system_events()
            mock_method.assert_called_with()

    def test_get_random_events(self):
        with patch.object(self.gs, '_get_random_events') as mock_method:
            self.gs._get_random_events()
            mock_method.assert_called_with()

    def test_draw_sprites(self):
        with patch.object(self.gs, '_draw_sprites') as mock_method:
            self.gs._draw_sprites()
            mock_method.assert_called_with()

    def test_update_screen(self):
        with patch.object(self.gs, '_update_screen') as mock_method:
            self.gs._update_screen()
            mock_method.assert_called_with()

    def test_check_level(self):
        with patch.object(self.gs, '_check_level') as mock_method:
            self.gs._check_level()
            mock_method.assert_called_with()

    def test_run_game(self):
        with patch.object(self.gs, 'run_game') as mock_method:
            self.gs.run_game()
            mock_method.assert_called_with()


if __name__ == "__main__":
    unittest.main()
