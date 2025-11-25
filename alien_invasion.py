import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Overall class to manange game assets and behaviour."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            #(self.settings.screen_width, self.settings.screen_height))
            (0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()
        
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()   # Watch for keyboard and mouse events.
            self.ship.update()     # Update ship's position 
            self._update_bullets() # Update bullets' postion
            self._update_screen()  # Redraw the screen during each pass through the loop.           
            self.clock.tick(60)

    def _check_events(self):
        """Helper function for managing events.Respond to keypresses and mouse events."""
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)

    def _update_screen(self):
        """Helper function for updating the screen during each pass through the loop.Update images on the screen,
           and flip
        """
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        pygame.display.flip()  # Make the most recently drawn screen visible.

    def _check_keydown_events(self,event):
        """Helper function for responding to keypresses (down)"""
        if event.key == pygame.K_RIGHT:
            # Move the ship to the right.
                self.ship.moving_right = True

        elif event.key == pygame.K_LEFT:
            # Move the ship to the left.
            self.ship.moving_left = True

        elif event.key == pygame.K_q:
            # 'Q' to quit game
            sys.exit()

        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self,event):
        """Helper function for responding to keyreleases (up)"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False

        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """update bullets' positions and delete old bullets"""
        # Update bullets' positions
        self.bullets.update()
        # Get rid of bullets that have disappeared.
        # Looping over a copy instead of original list bcoz python 
        # expects the list length to be same while the loop is still running
        for bullet in self.bullets.copy():       
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet) 

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and keep adding aliens until there's no room left.
        # Spacing between aliens is one alien width and one alien height.
        alien = Alien(self)
        alien_width = alien.rect.width
        alien_height = alien.rect.height

        current_x = alien_width
        current_y = alien_height

        while current_y < (self.settings.screen_height - 5 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            current_y += 2 * alien_height
            current_x = alien_width


    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the row"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)
    

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
