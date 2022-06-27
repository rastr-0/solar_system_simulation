import pygame
import math
pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (26, 209, 255)
RED = (255, 92, 51)
GREY = (80, 71, 81)
ORANGE = (204, 163, 0)

class Planet:
    # astronomical unit, distance from the Sun to the Earth in meters
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 80 / AU # 1 AU = 100 pixels
    TIMESTEP = 3600 * 24 # 1 day (3600 seconds = 1 hour)

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.sun = False
        self.distance_to_sun = 0
        self.orbit = []

        self.x_velocity = 0
        self.y_velocity = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))
        
            pygame.draw.lines(win, self.color, False, updated_points, 1)

        pygame.draw.circle(win, self.color, (x, y), self.radius)

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
        
        if other.sun:
            self.distance_to_sun = distance
        
        force = self.G * self.mass * other.mass / distance ** 2
        arc_tanget_angle = math.atan2(distance_y, distance_x)
        force_x = math.cos(arc_tanget_angle) * force
        force_y = math.sin(arc_tanget_angle) * force
        
        return force_x, force_y

    def update_position(self, planets):
        total_force_x = total_force_y = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_force_x += fx
            total_force_y += fy

        self.x_velocity += total_force_x / self.mass * self.TIMESTEP
        self.y_velocity += total_force_y / self.mass * self.TIMESTEP

        self.x += self.x_velocity * self.TIMESTEP
        self.y += self.y_velocity * self.TIMESTEP
        self.orbit.append((self.x, self.y))


def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 15, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 8, BLUE, 5.9742 * 10**24)
    earth.y_velocity = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 6, RED, 6.39 * 10**23)
    mars.y_velocity = 24.077 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 4, GREY, 0.330 * 10**23)
    mercury.y_velocity = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 7, WHITE, 4.8685 * 10**24)
    venus.y_velocity = -35.02 * 1000

    jupiter = Planet(5.2 * Planet.AU, 0, 10, ORANGE, 1.898 * 10**27)
    jupiter.y_velocity = -13.1 * 1000

    planets = [sun, earth, mars, mercury, venus, jupiter]

    while run:
        clock.tick(60)
        WIN.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)
        pygame.display.update()

    pygame.quit()


main()
