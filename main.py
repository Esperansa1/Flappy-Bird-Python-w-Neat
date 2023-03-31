import os
import neat
import pygame
import pickle
from Bird import Bird
from PillarManager import PillarManager
from random import randint
import sys
WHITE = (255, 255, 255)

pygame.init()
pygame.display.set_caption('Flappy Bird AI')

fps = 60
clock = pygame.time.Clock()

WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pillar_manager = PillarManager(screen, WIDTH, HEIGHT)
score = 0
birds = []
dead_birds = []


def is_collided(bird):
    pillars = pillar_manager.pillars
    for pillar in pillars:
        bird_x, bird_y = bird.pos
        if (bird_y+20 > pillar.y+pillar.gap or bird_y-20 < pillar.y-pillar.gap) and bird_x+20 >= pillar.x and bird_x-20 <= pillar.x + 50:
            return True

    if bird_y + 20 > HEIGHT or bird_y - 20 < 0:
        return True

    return False


def update_score():
    global score
    for pillar in pillar_manager.pillars:
        if pillar.x == 120:
            score += 1


def draw_screen(bird):
    screen.fill(WHITE)
    bird.draw()
    pillar_manager.draw_pillars()
    font = pygame.font.SysFont('freesansbold.ttf', 72)
    text = font.render(f'Score: {score}', True, (255, 0, 0))
    screen.blit(text, (50, 50))


def move(bird):
    bird.move()
    pillar_manager.move_pillars()


def run(bird):
    running = True
    while running:
        clock.tick(60)
        update_score()
        draw_screen(bird)
        move(bird)

        if is_collided(bird):
            running = False

        closest_pillar = get_closest_pillar(bird)
        output = bird.brain.activate(
            (closest_pillar.top, closest_pillar.bottom, bird.y))
        if output[0] > 0.5:
            bird.flap()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()


def get_closest_pillar(bird):
    pillars = pillar_manager.pillars
    min_dist = 10000
    closest_pillar = None
    for pillar in pillars:
        if pillar.x+55 >= bird.x and pillar.x < min_dist:
            min_dist = pillar.x
            closest_pillar = pillar
    return closest_pillar


def train_ai(genomes, config):
    global score

    score = 0
    birds = []
    for genome_id, genome in genomes:
        if genome.fitness == None:
            genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        birds.append(Bird(screen, (100, HEIGHT//2), net, genome))

    run = True
    while run:
        clock.tick(60)
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        closest_pillar = get_closest_pillar(birds[0])
        for bird in birds:

            output = bird.brain.activate(
                (closest_pillar.top, closest_pillar.bottom, bird.y))
            if output[0] > 0.5:
                bird.flap()

            bird.draw()
            bird.move()
            if is_collided(bird):
                bird.genome.fitness = score
                birds.remove(bird)

        pillar_manager.move_pillars()
        pillar_manager.draw_pillars()
        font = pygame.font.SysFont('freesansbold.ttf', 72)
        text = font.render(f'Score: {score}', True, (255, 0, 0))
        screen.blit(text, (50, 50))

        update_score()

        pygame.display.update()
        if len(birds) == 0:
            run = False
            pillar_manager.restart_pillars()


def test_ai(config):
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)
    net = neat.nn.FeedForwardNetwork.create(winner, config)
    run(Bird(screen, (100, HEIGHT//2), net, winner))


def run_neat():
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    winner = p.run(train_ai)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    run_neat()
    # test_ai(config)
