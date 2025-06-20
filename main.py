import pygame
import random

pygame.init()


WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Circles")

pygame.font.init()
font = pygame.font.SysFont('Arial', 20)

pygame.mixer.init()  # Initialize the sound mixer

# Load the bell sound
# Make sure bell.wav is in the same folder as main.py
bell = pygame.mixer.Sound('bell.wav')
bell.set_volume(0.5)  # Set the volume (0.0 to 1.0)


clock = pygame.time.Clock()
fps = 60  # Frames per second

# Set the background color to white
screen.fill((255, 255, 255))


class Circle:
    def __init__(self, x, y, radius, color, speed_x, speed_y, damping_factor):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed_x = random.uniform(-10, 10)
        self.speed_y = random.uniform(-10, 10)
        self.damping_factor = damping_factor

        self.last_stimulus_time = 0
        self.sensitivity = 1  # Initial sensitivity

    def draw(self):
        pygame.draw.circle(
            surface=screen,
            color=self.color,
            center=(self.x, self.y),
            radius=self.radius
        )

    def move(self):
        # self.speed_x = self.speed_x + random.uniform(-0.2,0.2)  # Random speed in x direction
        # self.speed_y = self.speed_y + random.uniform(-0.2,0.2)

        self.speed_x = self.speed_x * self.damping_factor
        self.speed_y = self.speed_y * self.damping_factor

        self.x = self.x + int(self.speed_x)
        self.y = self.y + int(self.speed_y)

        self.x %= WIDTH  # Wrap around the screen horizontally
        self.y %= HEIGHT  # Wrap around the screen vertically

    def reactivate(self, current_time):

        time_since_last_stimulus = current_time - self.last_stimulus_time

        if time_since_last_stimulus < 2000:  # 2 second
            self.sensitivity *= 0.9  # Decrease sensitivity
        # else:
        #     self.sensitivity = min(
        #         1, self.sensitivity + 0.01 * (time_since_last_stimulus // 1000))

        self.last_stimulus_time = current_time

        self.speed_x = random.uniform(-10, 10) * self.sensitivity
        self.speed_y = random.uniform(-10, 10) * self.sensitivity


# Set the initial position and radius of the circle
x, y = (300, 300)  # Center of the screen
radius = 50  # Radius of the circle
# Create a Circle object
damping_factor = 0.98
# circle = Circle(x, y, radius, (255, 0, 0), 1, -1,damping_factor)

# LAB 3
# Space is uncoditional stimulus, bell is a neutral stimilus initally,
# then we paired it as a conditional stimulus
pairings = []
conditioning_threshold = 3
cs_learned = False


extinction_threshold = 5
cs_only_trials = 0
cs_extinguished = False

recovery_threshold = 5000  
extinction_time = None
recovered = False

circles = []
for _ in range(10):
    circle = Circle(x=random.randint(0, WIDTH), y=random.randint(0, HEIGHT), radius=random.randint(10, 50), color=(random.randint(0, 255), random.randint(
        0, 255), random.randint(0, 255)), speed_x=random.uniform(-10, 10), speed_y=random.uniform(-10, 10), damping_factor=damping_factor)
    circles.append(circle)

start_time = pygame.time.get_ticks()  # Get the current time in milliseconds

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                current_time = pygame.time.get_ticks()
                for circle in circles:
                    circle.reactivate(current_time)
                pairings.append(("UCS", current_time))
            if event.key == pygame.K_b:
                current_time = pygame.time.get_ticks()
                bell.play()

                pairings.append(("CS", current_time))

                ucs_times = [t for k, t in pairings if k == "UCS"]
                cs_times = [t for k, t in pairings if k == "CS"]

                recent_pairings = [
                    (cs, ucs)
                    for cs in cs_times
                    for ucs in ucs_times
                    if 0 < ucs - cs <= 1000
                ]

                if len(recent_pairings) >= conditioning_threshold:
                    cs_learned = True
                if cs_learned:

                    #Lab 4    
                    recent_ucs = [t for k, t in pairings if k == "UCS" and 0 < current_time - t <= 1000]
                    if not recent_ucs:
                        cs_only_trials +=1
                        if cs_only_trials < extinction_threshold:
                            for circle in circles:
                                circle.reactivate(current_time)
                        else:
                            cs_learned = False
                            cs_extinguished = True    
                            extinction_time = current_time                              
                    else:
                        cs_only_trials = 0
                        for circle in circles:
                            circle.reactivate(current_time)
                                        

                    # for circle in circles:
                    #     circle.reactivate(current_time)

    screen.fill((255, 255, 255))

    current_tick = pygame.time.get_ticks()  # Get the current time in milliseconds
    elapsed_time = (current_tick - start_time) // 1000  # Convert to seconds

    if cs_extinguished and extinction_time is not None:
        time_since_extinction = current_tick - extinction_time
        if time_since_extinction >= recovery_threshold:
            recovered = True
            cs_extinguished = False
            cs_learned = True
            cs_only_trials = 0            

    # avg_sensitity = sum(
    #     circle.sensitivity for circle in circles) / len(circles)
    # avg_sensitity_text = f"Avg Sensitivity: {avg_sensitity:.3f}"

    elapsed_time_text = f"Elapsed Time: {elapsed_time:.2f} seconds"
    cs_learned_text = f"CS Learned: {cs_learned}"
    cs_extinction_text = f"CS Extinction Trials: {cs_extinguished}"
    recovered_text = f"CS Recovered: {recovered}"

 
    # text = elapsed_time_text + "\n" + avg_sensitity_text
    text = elapsed_time_text + "\n" + cs_learned_text + "\n" + cs_extinction_text + "\n" + recovered_text
    rendered_text = font.render(text, True, (0, 0, 0))


# Draw a red circle
# A red circle is drawn using pygame.draw.circle() with these parameters:
# screen: the surface to draw on
# (255, 0, 0): RGB values for red
# (300, 300): center position of the circle (middle of the 600x600 window)
# 50: radius of the circle in pixels

    # x+= 1  # Move the circle to the right
    # y-= 1  # Move the circle down
    # pygame.draw.circle(surface=screen, color=(255, 0, 0), center=(x,y), radius=radius)

    for circle in circles:
        circle.draw()  # Draw the circle on the screen
        circle.move()  # Move the circle


# updates the display to show the changes. This is crucial as Pygame uses double buffering
    screen.blit(rendered_text, (10, 10))  # Draw the text on the screen
    pygame.display.flip()

    clock.tick(fps)  # Set the frame rate

pygame.quit()
