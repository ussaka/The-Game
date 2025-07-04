import pygame
import random
import asyncio


# Set and get player's coordinates
class Player:
    def __init__(self, x, y) -> None:
        self.__x = x
        self.__y = y

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        self.__x = value

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value):
        self.__y = value


class The_Game:
    def __init__(self) -> None:
        pygame.init()
        self.__display_width = 1280
        self.__display_height = 720
        self.display = pygame.display.set_mode(
            (self.__display_width, self.__display_height)
        )
        self.load_images()
        self.load_items_to_be_dropped()

        self.key_down_up = False
        self.key_down_left = False
        self.key_down_right = False

        self.score = 0
        self.high_score = 0
        self.player = Player(
            self.__display_width / 2 - (self.robot_width / 2),
            self.__display_height / 2 - (self.robot_height / 2),
        )
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("Comic Sans", 30)
        self.font2 = pygame.font.SysFont("Comic Sans", 180)
        pygame.display.set_caption("The Game")

        self.running = True

    def load_images(self):
        self.images = {}
        for name in ["hirvio", "kolikko", "ovi", "robo"]:
            self.images[name] = pygame.image.load(name + ".png")

        self.robot_width = self.images["robo"].get_width()
        self.robot_height = self.images["robo"].get_height()
        self.monster_width = self.images["hirvio"].get_width()
        self.monster_height = self.images["hirvio"].get_height()
        self.coin_width = self.images["kolikko"].get_width()
        self.coin_height = self.images["kolikko"].get_height()
        self.door_width = self.images["ovi"].get_width()
        self.door_height = self.images["ovi"].get_height()

    def load_items_to_be_dropped(self):
        self.monsters_pcs = 11
        self.monsters = []
        # Start coordinates outside display
        for i in range(self.monsters_pcs):
            # (x, y, direction to move(left or right))
            self.monsters.append([-1000, self.__display_height, random.choice((-1, 1))])

        self.coins_pcs = 5
        self.coins = []
        for i in range(self.coins_pcs):
            self.coins.append([-1000, self.__display_height])

        self.doors_pcs = 1
        self.doors = []
        for i in range(self.doors_pcs):
            self.doors.append([-1000, self.__display_height])

    async def game_loop(self):
        while self.running:
            self.player_movement()
            self.items_location()
            self.draw_display()
            await asyncio.sleep(0)  # Allow browser to handle other tasks

    def draw_display(self):
        self.display.fill((51, 52, 50))

        score_txt = self.font.render(f"Score: {self.score}", True, (244, 96, 54))
        self.display.blit(score_txt, (1100, 60))
        high_score_txt = self.font.render(
            f"High Score: {self.high_score}", True, (255, 251, 70)
        )
        self.display.blit(high_score_txt, (1015, 20))

        self.display.blit(self.images["robo"], (self.player.x, self.player.y))

        # Collision with monster. If score is negative --> Game Over
        for i in range(self.monsters_pcs):
            self.display.blit(
                self.images["hirvio"], (self.monsters[i][0], self.monsters[i][1])
            )
            if (
                self.player.x
                <= self.monsters[i][0] + (self.monster_width / 2)
                <= self.player.x + self.robot_width
            ):
                if (
                    self.player.y
                    <= self.monsters[i][1]
                    <= self.player.y + self.robot_height
                    or self.player.y
                    <= self.monsters[i][1] + self.monster_height
                    <= self.player.y + self.robot_height
                ):
                    if self.score < 0:
                        game_over_txt = self.font2.render(
                            "GAME OVER", True, (244, 96, 54)
                        )
                        self.display.blit(
                            game_over_txt,
                            (
                                self.__display_width / 2
                                - game_over_txt.get_width() / 2,
                                self.__display_height / 2
                                - game_over_txt.get_height() / 2,
                            ),
                        )
                        pygame.display.flip()
                        self.clock.tick(1)
                        self.clock.tick(1)
                        self.game_over()
                    else:
                        self.monsters[i][1] = 1500  # Move out of sight
                        self.score -= 10
        # Collision with coins
        for i in range(self.coins_pcs):
            self.display.blit(
                self.images["kolikko"], (self.coins[i][0], self.coins[i][1])
            )
            if (
                self.player.x
                <= self.coins[i][0] + (self.coin_width / 2)
                <= self.player.x + self.robot_width
            ):
                if (
                    self.player.y
                    <= self.coins[i][1]
                    <= self.player.y + self.robot_height
                    or self.player.y
                    <= self.coins[i][1] + self.coin_height
                    <= self.player.y + self.robot_height
                ):
                    self.coins[i][1] = 1500  # Move out of sight
                    self.score += 1
        # Collision with door --> save high score and restart the game
        for i in range(self.doors_pcs):
            self.display.blit(self.images["ovi"], (self.doors[i][0], self.doors[i][1]))
            if (
                self.player.x
                <= self.doors[i][0] + (self.door_width / 2)
                <= self.player.x + self.robot_width
            ):
                if (
                    self.player.y
                    <= self.doors[i][1]
                    <= self.player.y + self.robot_height
                    or self.player.y
                    <= self.doors[i][1] + self.door_height
                    <= self.player.y + self.robot_height
                ):
                    self.game_over()

        pygame.display.flip()
        self.clock.tick(120)

    def player_movement(self):
        for evt in pygame.event.get():
            if evt.type == pygame.KEYDOWN:
                if evt.key == pygame.K_LEFT:
                    self.key_down_left = True
                if evt.key == pygame.K_RIGHT:
                    self.key_down_right = True
                if evt.key == pygame.K_UP:
                    self.key_down_up = True

            if evt.type == pygame.KEYUP:
                if evt.key == pygame.K_LEFT:
                    self.key_down_left = False
                if evt.key == pygame.K_RIGHT:
                    self.key_down_right = False
                if evt.key == pygame.K_UP:
                    self.key_down_up = False

            if evt.type == pygame.QUIT:
                self.running = False

        # Move left or right
        if self.player.x + self.robot_width != self.__display_width:
            if self.key_down_right:
                self.player.x += 5
        if self.player.x != 0:
            if self.key_down_left:
                self.player.x -= 5

        # Jump
        if self.player.y != 0:
            if (
                self.key_down_up
                and self.player.y + self.robot_height == self.__display_height
            ):
                self.player.y -= 120
        if self.player.y + self.robot_height != self.__display_height:
            self.player.y += 1

    def items_location(self):
        for i in range(self.monsters_pcs):
            if self.monsters[i][1] + self.monster_height != self.__display_height:
                self.monsters[i][1] += 1
            elif self.monsters[i][1] == (self.__display_height - self.monster_height):
                # Move left or right
                if self.monsters[i][2] == 1:
                    self.monsters[i][0] += 1
                elif self.monsters[i][2] == -1:
                    self.monsters[i][0] -= 1

            if (
                self.monsters[i][1] > self.__display_height
                or self.monsters[i][0] > self.__display_width
                or self.monsters[i][0] < 0
            ):
                self.monsters[i][0] = random.randint(
                    0, self.__display_width - self.monster_width
                )
                self.monsters[i][1] = -random.randint(200, 500)

        for i in range(self.coins_pcs):
            self.coins[i][1] += 2
            if self.coins[i][1] > self.__display_height:
                self.coins[i][0] = random.randint(
                    0, self.__display_width - self.coin_width
                )
                self.coins[i][1] = -random.randint(400, 800)

        for i in range(self.doors_pcs):
            self.doors[i][1] += 2
            if self.doors[i][1] > self.__display_height:
                self.doors[i][0] = random.randint(
                    0, self.__display_width - self.door_width
                )
                self.doors[i][1] = -random.randint(500, 1000)

    def game_over(self):
        if self.score >= self.high_score:
            self.high_score = self.score
        self.load_items_to_be_dropped()
        self.score = 0


async def main():
    game = The_Game()
    await game.game_loop()


if __name__ == "__main__":
    asyncio.run(main())
