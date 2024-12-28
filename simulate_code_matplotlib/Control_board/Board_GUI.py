import pygame





class Graphics:
    def __init__(self, dimentions, map_img_path = None):
        pygame.init()

        # Colors
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.red = (255, 0, 0)
        self.yel = (255, 255, 0)
        self.steel_blue = (70,130,180)
        self.royal_blue = (65,105,225)
        self.sky_blue = (135,206,235)
        self.gainsboro = (220,220,220)                              # ligth gray
        self.white_smoke = (245,245,245)     
        self.crimson = (220,20,60)     
        self.light_coral = (240,128,128)
        self.medium_aqua_marine = (102,205,170)
        self.plum = (221,160,221)
        self.light_steel_blue = (176,196,222)
        self.slate_gray = (112,128,144)
        self.mint_cream =  	(245,255,250)
        self.navajo_white = (255,222,173)
        # https://www.rapidtables.com/web/color/RGB_Color.html

        # Window
        self.width, self.height = dimentions
        self.map_img = pygame.image.load(map_img_path)

        # Set init. settings
        pygame.display.set_caption("Electrodes Board")
        self.map = pygame.display.set_mode((self.width, self.height))
        self.map.blit(self.map_img, (0,0))

        # Output
        self.path_list = []

        # Electrodes 
        self.num_divices = 4
        self.num_pins_divices = 8           
        self.electro_w = 50
        self.electro_h = 50
        self.distance_between = 25
        self.init_pint_electrodes_x = int(self.width/2) - int((self.num_pins_divices/2)*(self.electro_w+self.distance_between))     # (x, y) upper-left corner for the board (first electrode)
        self.init_pint_electrodes_y = int(self.height/2) - int((self.num_divices/2)*(self.electro_h+self.distance_between))
        self.electrodes_rect_list = []
        self.rect_flag_list = []

        self.font_electrodes = pygame.font.Font(None, 25)
        self.electrodes_text_list = []

        # rect( x_up, y_up, width, height )
        # self.electrodes_rect_list = [
            # {"id": 0, "rect": pygame.Rect((600, 300), (100, 50))} ]                


        # Create electrodes rectangles
        for i in range(0, self.num_divices*self.num_pins_divices):
            row = int(i/self.num_pins_divices)
            colmn = int(i%self.num_pins_divices)

            x_pos = colmn*(self.distance_between+self.electro_w) + self.init_pint_electrodes_x
            y_pos = row*(self.distance_between+self.electro_h) + self.init_pint_electrodes_y

            self.electrodes_rect_list.append({"id": i, "rect": pygame.Rect((x_pos, y_pos), (self.electro_w, self.electro_h))})
            self.rect_flag_list.append(0)

            # Text to draw the id
            text = self.font_electrodes.render(str(i), 1, self.black )
            text_pos = text.get_rect()
            text_pos.center = ( x_pos+int(self.electro_w/2), y_pos + int(self.electro_h/2) )
            self.electrodes_text_list.append({"id": i, "text": text, "text_pos": text_pos })


        # Draw stored numbers (electrodes's ids)
        self.font_select_ids = pygame.font.Font(None, 36)
        self.path_text_list = []
        self.x_store_ids_text = 200
        self.y_store_ids_text = self.height - 50
        self.distance_ids_text = 50

    
    def number2text_store(self, id):
        '''
            Store the id electrode selected in text form to be display in the window
        '''

        length = len(self.path_text_list)

        text = self.font_select_ids.render(str(id), 1, self.crimson )
        text_pos = text.get_rect()
        x_pos = self.x_store_ids_text+( length*self.distance_ids_text )
        text_pos.center = ( x_pos , self.y_store_ids_text )
        self.path_text_list.append({"id": length, "text": text, "text_pos": text_pos })

        # print("text path x pos = ", x_pos, length)



    def draw_board(self):
        color_rect =  self.navajo_white

        # Draw electrodes (rectangle shape)
        for rect_electro in self.electrodes_rect_list:
            if self.rect_flag_list[rect_electro['id']] :
                color_rect = self.sky_blue
            else:
                color_rect =  self.navajo_white

            # pygame.draw.rect(self.map, self.navajo_white, rect_electro["rect"] )
            pygame.draw.rect(self.map, color_rect, rect_electro["rect"] )

        for text_electro in self.electrodes_text_list:
            # draw rect text
            self.map.blit(text_electro["text"], text_electro["text_pos"])

        for text_path in self.path_text_list:
            self.map.blit(text_path["text"], text_path["text_pos"])


        # Delete path botton
        # pygame.draw.rect(self.map, self.navajo_white, 
        #                     pygame.Rect( rect_electro[0], rect_electro[1], rect_electro[2], rect_electro[3] ))
            
    

    def dectect_actions(self):
        running = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  

            # checking if keydown event happened or not
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_q:
                    running = False  

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()                       # Get click position

                for rect_electro in self.electrodes_rect_list: 
                    if rect_electro["rect"].collidepoint(x, y):    
                        id_electro = rect_electro["id"] 
                        print("Click over electrode = ", id_electro)
                        
                        self.path_list.append(id_electro)
                        self.rect_flag_list[id_electro] = 1

                        # store the id selected to draw the text
                        self.number2text_store(id_electro)

        return running
    