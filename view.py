import curses
from model import Choice


class View:
    def __init__(self, controler):
        self.running = False
        self.controler = controler

    def init_windows(self, screen):
        self.screen = screen
        self.help_window = curses.newwin(6, 13, 0, 0)
        self.result_window = curses.newwin(6, 15, 0, 25)
        self.stats_window = curses.newwin(25, curses.COLS - 1, 8, 0)

    def init_terminal(self):
        curses.curs_set(0)

    def stop(self):
        self.running = False

    def render_ui(self, screen):
        screen.clear()
        self.init_terminal()
        self.init_windows(screen)
        
        screen.refresh()

        while self.running:
            self.print_help()
            player_choice = self.get_intput()
            if not player_choice:
                return self.stop()
            result = self.controler.play(player_choice)
            self.print_result(result)
            self.print_stats(screen)

    def print_stats(self, screen):
        self.stats_window.clear()

        line = 0
        self.stats_window.addstr(line, 0, 'AI STATS:')
        line += 2
        self.stats_window.addstr(line, 0, 'Global:')
        line += 1

        if self.controler.stats.resolved_games > 0:
            self.stats_window.addstr(line, 0, f'Wins {self.controler.stats.wins} ({self.controler.stats.win_rate * 100:.3f}%)')
            line += 1
            self.stats_window.addstr(line, 0, f'Losses {self.controler.stats.loses} ({self.controler.stats.loss_rate * 100:.3f}%)')
            line += 1

        for ai in self.controler.ais:
            if ai.stats.resolved_games > 0:
                line += 1
                self.stats_window.addstr(line, 0, str(ai))
                line += 1
                self.stats_window.addstr(line, 0, f'Wins {ai.stats.wins} ({ai.stats.win_rate * 100:.3f}%)')
                line += 1
                self.stats_window.addstr(line, 0, f'Losses {ai.stats.loses} ({ai.stats.loss_rate * 100:.3f}%)')
            line += 1


        self.stats_window.refresh()

    def print_result(self, result):
        self.result_window.clear()
        self.result_window.addstr(0, 0, f'You: {result.player_choice.name}')
        self.result_window.addstr(1, 0, f'PC:  {result.ai_choice.name}')
        if result.player_wins:
            text = 'You win!'
        elif result.ai_wins:
            text = 'You lose!'
        else:
            text = 'Draw!'
        self.result_window.addstr(2, 0, text)
        self.result_window.refresh()

    def print_help(self):
        self.help_window.clear()
        line = 0
        self.help_window.addstr(line, 0, 'Press a key:')
        line += 1
        for choice in Choice:
            self.help_window.addstr(line, 0, f'[{choice.value}] {choice.name}')
            line += 1
        self.help_window.addstr(line, 0, f'[x] Quit')
        self.help_window.refresh()

    def get_intput(self):
        while True:
            key = self.screen.getkey()
            if key == 'x':
                return None
            elif key in [str(c.value) for c in Choice]:
                return Choice(int(key))

    def run(self):
        try:
            self.running = True
            curses.wrapper(self.render_ui)
        except KeyboardInterrupt:
            pass