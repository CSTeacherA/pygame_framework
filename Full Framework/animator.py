import pygame


class Animator:
    def __init__(self, spritesheet, rows, columns):
        """
        spritesheet : pygame.Surface
        rows        : number of animation rows
        columns     : number of frames per row
        """

        self.spritesheet = spritesheet
        self.rows = rows
        self.columns = columns

        self.frames = []
        self._slice_sheet()

        self.current_row = 0
        self.current_col = 0

        self.fps = 8
        self.timer = 0
        self.playing = False

    # ----------------------------
    # Slice Spritesheet
    # ----------------------------
    def _slice_sheet(self):
        sheet_width = self.spritesheet.get_width()
        sheet_height = self.spritesheet.get_height()

        frame_width = sheet_width // self.columns
        frame_height = sheet_height // self.rows

        for row in range(self.rows):
            row_frames = []
            for col in range(self.columns):
                rect = pygame.Rect(
                    col * frame_width,
                    row * frame_height,
                    frame_width,
                    frame_height
                )
                image = self.spritesheet.subsurface(rect).copy()
                row_frames.append(image)
            self.frames.append(row_frames)

    # ----------------------------
    # Control Animation
    # ----------------------------
    def play(self, row, fps=8, column_limit=None):
        self.column_limit = column_limit    
        self.current_row = row
        self.fps = fps
        self.playing = True

    def play_reset(self, row, fps=8):
        self.current_col = 0 # reset column 
        self.play(row, fps)


    def stop(self):
        self.playing = False

    # ----------------------------
    # Update Animation
    # ----------------------------
    def update(self, dt):
        if not self.playing:
            return

        self.timer += dt

        if self.timer >= 1 / self.fps:
            self.timer = 0
            self.current_col += 1

            if self.current_col >= self.columns or (self.column_limit and self.current_col >= self.column_limit):
                self.current_col = 0

    # ----------------------------
    # Accessors
    # ----------------------------
    def get_frame(self, row, col):
        if row >= self.rows or col >= self.columns:
            print("Out of range:", row, col, "must be within:", self.rows,self.columns)
            return self.get_current_frame()
        return self.frames[row][col]

    def get_current_frame(self):
        return self.frames[self.current_row][self.current_col]
    
    def set_current_column(self, col):
        if col >= self.columns or col < 0:
            print("Out of range:", col, "must be within:", self.columns)
            return
        self.current_col = col