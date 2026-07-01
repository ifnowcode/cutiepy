import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox
from matplotlib import colors
import PIL.ImageTk
from PIL import Image, ImageFilter, ImageOps, ImageFile, ImageColor, ImageDraw, ImageFont
from PIL.ExifTags import TAGS
#ImageFile.LOAD_TRUNCATED_IMAGES = True
import sys
import os
import shutil
import argparse
import winreg
import time
import threading
import random
import math
import ntpath
from datetime import datetime, timedelta
import uuid
import cv2
import io
import base64
import numpy as np
import ctypes
from ctypes import wintypes
import tempfile
from enum import Enum, IntEnum, auto, unique
import inspect
from walker import crawltree
from printcon import *
# [RULE] TODO: pri=0;sev=0;  {assert sev <= pri}
# https://gist.github.com/nakagami/3764702

# Difference between a Picture an Image and a Photo
# https://difference.guru/difference-between-picture-image-and-photo/

# PIL RTFM
# https://pillow.readthedocs.io/en/stable/reference/Image.html
# https://pillow.readthedocs.io/en/5.1.x/reference/Image.html
# https://python-pillow.org/pillow-perf/

# tkinter
# https://docs.python.org/3/library/tkinter.html
# https://stackoverflow.com/questions/42834675/base64-string-to-image-in-tkinter

# Tkinter Attributes
# https://www.delftstack.com/howto/python-tkinter/how-to-create-full-screen-window-in-tkinter/

# Blur https://stackoverflow.com/questions/21215903/blurring-an-image-using-pil-in-python
# Examples: https://www.programcreek.com/python/example/57116/PIL.ImageFilter.BLUR

# Custom Filters etc.
# https://stackoverflow.com/questions/3346980/how-do-the-pil-imagefilter-enhancement-filters-work
# https://pillow.readthedocs.io/en/stable/reference/ImageFilter.html

# Gray Scale
# https://appdividend.com/2020/06/22/how-to-convert-pil-image-to-grayscale-in-python/

# PIL Filter reference
# https://pillow.readthedocs.io/en/stable/reference/ImageFilter.html

# Image convert and dithering
# https://www.geeksforgeeks.org/python-pil-image-convert-method/
# https://www.newbedev.com/image-conversion-in-python-using-pil-png-jpg-webp-png/
# https://research.cs.wisc.edu/graphics/Courses/559-s2004/docs/floyd-steinberg.pdf
# https://www.visgraf.impa.br/Courses/ip00/proj/Dithering1/floyd_steinberg_dithering.html

# Test Images
# https://testimages.org/
# https://en.wikipedia.org/wiki/Standard_test_image
# https://filesamples.com/formats/ppm

# TODO: pri=0;sev=0; image cropping, fonts, drawing? what can PIL do? This should be called pilbox.py
# TODO: pri=0;sev=0; Update window to display thumbs like explorer that allows selection of the thumb for full size display

# TODO: use fonts and print out help info on 'F1' showing all the shortcuts 'F2' all the commands and when the app is started and stopped etc. it will for 1 or 2 seconds display a message indicating the state change or action taken.

# TODO: display an error image for unsupported media type

# TODO: Collage mode with multiple overlapping transparent images. Do a whole directory at one time?

# Events
# http://www.tcl.tk/man/tcl8.4/TkCmd/keysyms.htm
# https://web.archive.org/web/20190512164300id_/http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/event-types.html

# PIL Tricks - Thumnail, Replace Colors, Add Borders, Blur Edges, Add Watermark
# https://pillow.readthedocs.io/en/3.0.x/reference/Image.html
# https://pillow.readthedocs.io/en/stable/reference/Image.html
# https://medium.com/analytics-vidhya/some-interesting-tricks-in-python-pillow-8fe5acce6084
# https://pillow.readthedocs.io/en/stable/reference/Image.html
# https://note.nkmk.me/en/python-pillow-gif/
# https://stackoverflow.com/questions/17223854/displaying-animated-gifs-in-tkinter-using-pil
# https://web.archive.org/web/20200705080256id_/http://effbot.orfg/imagingbook/introduction.htm
# https://iq.opengenus.org/images-in-python-pil/ ?
# https://holypython.com/image-manipulation-with-python-pil/
# https://note.nkmk.me/en/python-pillow-paste/
# https://www.programcreek.com/python/example/89905/PIL.Image.Image
# https://pythonexamples.org/python-pillow-adjust-image-contrast/
# https://www.geeksforgeeks.org/python-pil-imageenhance-color-and-imageenhance-contrast-method/

# PhotoImage
# https://www.programcreek.com/python/example/64885/PIL.ImageTk.PhotoImage

# Images
# https://www.c-sharpcorner.com/Blogs/basics-for-displaying-image-in-tkinter-python

# OpenCV (sample: cv.py)
# https://www.life2coding.com/play-video-files-using-opencv-python/
# https://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html#videocapture-get
# https://www.pyimagesearch.com/2017/02/06/faster-video-file-fps-with-cv2-videocapture-and-opencv/
# https://www.programcreek.com/python/example/85663/cv2.VideoCapture

# Machine/Deep Learning
# https://www.bigrabbitdata.com/pytorch-3-tensor-and-images/
# https://machinelearningmastery.com/how-to-load-and-manipulate-images-for-deep-learning-in-python-with-pil-pillow/

# Keras
# https://machinelearningmastery.com/how-to-normalize-center-and-standardize-images-with-the-imagedatagenerator-in-keras/

# PPM
# https://people.cs.clemson.edu/~yfeaste/cpsc101/CPSC101F15Yvon/Lectures/Oct1-ppm/PPM_Images.pdf
# http://paulbourke.net/dataformats/ppm/

# Paths
# https://medium.com/@ageitgey/python-3-quick-tip-the-easy-way-to-deal-with-file-paths-on-windows-mac-and-linux-11a072b58d5f

# Grid
# https://www.geeksforgeeks.org/python-tkinter-grid_location-and-grid_size-method/

class Cutie(Frame):
    # https://www.tutorialspoint.com/python/tk_frame.htm
    filters = {'ImageFilter.CONTOUR': ImageFilter.CONTOUR,
               'ImageFilter.DETAIL': ImageFilter.DETAIL,
               'ImageFilter.EDGE_ENHANCE': ImageFilter.EDGE_ENHANCE,
               'ImageFilter.EDGE_ENHANCE_MORE': ImageFilter.EDGE_ENHANCE_MORE,
               'ImageFilter.EMBOSS': ImageFilter.EMBOSS,
               'ImageFilter.FIND_EDGES': ImageFilter.FIND_EDGES,
               'ImageFilter.SHARPEN': ImageFilter.SHARPEN,
               'ImageFilter.SMOOTH': ImageFilter.SMOOTH,
               'ImageFilter.SMOOTH_MORE': ImageFilter.SMOOTH_MORE}

    windows_geometries = {'tool': {'width': 108, 'height':30},
                          'widget': {'width': 108, 'height':116},
                          'compact': {'width': 640, 'height':480},
                          'normal': {'width': 976, 'height':549},
                          'widescreen': {'width': 1200, 'height':600}}

    class eCap(IntEnum):
        CV_CAP_PROP_POS_MSEC = 0,
        CV_CAP_PROP_POS_FRAMES = 1,     # in OpenCV 3.0 this is change to CAP_PROP_POS_FRAMES, don't know the value
        CV_CAP_PROP_POS_AVI_RATIO = 2,
        CV_CAP_PROP_FRAME_WIDTH = 3,
        CV_CAP_PROP_FRAME_HEIGHT = 4,
        CV_CAP_PROP_FPS = 5,
        CV_CAP_PROP_FOURCC = 6,
        CV_CAP_PROP_FRAME_COUNT = 7,
        CV_CAP_PROP_FORMAT = 8,
        CV_CAP_PROP_MODE = 9,
        CV_CAP_PROP_BRIGHTNESS = 10,
        CV_CAP_PROP_CONTRAST = 11,
        CV_CAP_PROP_SATURATION = 12,
        CV_CAP_PROP_HUE = 13,
        CV_CAP_PROP_GAIN = 14,
        CV_CAP_PROP_EXPOSURE = 15,
        CV_CAP_PROP_CONVERT_RGB = 16,
        CV_CAP_PROP_WHITE_BALANCE = 17,
        CV_CAP_PROP_RECTIFICATION = 18,
        #CV_CAP_PROP_BUFFERSIZE = ?,
        #CV_CAP_PROP_WHITE_BALANCE_U = ?,     # note: only supported by DC1394 v 2.x backend currently
        #CV_CAP_PROP_WHITE_BALANCE_V = ?,     # note: only supported by DC1394 v 2.x backend currently
        #CV_CAP_PROP_RECTIFICATION = ?,       # note: only supported by DC1394 v 2.x backend currently
        #CV_CAP_PROP_ISO_SPEED = ?,           # note: only supported by DC1394 v 2.x backend currently


    @trace(1)
    def __init__(self, targets, showfile=False, inspector=True, debug=False):
      perftime = datetime.now()
      loginfo("Initializing Object")
      # https://www.mytecbits.com/internet/python/addition-and-subtraction-of-time
      #newtime = currtime + timedelta(seconds=self.interval)
      # TODO: make functions to set these break_on_error(True), etc. This is for diagnostics.py
      self.targets = targets
      self.inspection_mode = inspector
      self.rawimg = None
      self.filtimg = None
      self.effimg = None
      self.sizedimg = None
      self.pilimg = None
      self.dirname = None
      self.num_page = 0
      self.framecntr = None
      self.framerate = None
      self.tracelevel  = ''
      self.bblevel = ''
      self.filenamepath = ''
      self.filenamepathlbltext = None
      self.file_ext = ''
      self.file_name = ''
      self.isources = 0
      self.sources = []
      self.iordered_sources = 0
      self.ordered_sources = []
      self.shuffle = False
      self.ishuffled_sources = 0
      self.shuffled_sources = []
      self.root_directory = None
      self.ifilter_history = 0
      self.filter_history = []
      self.icommand_history = 0
      self.command_history = []
      self.ishortcuts = 0
      self.shortcuts = {}
      self.ihistory = 0
      self.history = []
      self.timer = None
      self.showbtn = None
      self.repeat = False
      self.resize = True
      self.interval = 4
      self.interval_incdec = 2
      self.random = False
      self.sortbydate = True
      self.reverse_sort = True
      self.showfile = showfile
      self.debug = False
      # TODO: show_debug = True # add show_debug for release mode to remove the (i) debug button and shortcuts etc. so it can't be accessed at all
      self.privacy = False # a 100% blur filter is controlled seperately and initially set for security
      # removed BLUR from filters as it only makes the pictures worse and i can
      # always apply it after the fact to see if there is any improvment (there won't be)
      # made a dict to be able to look them up for commands like help, [ref] https://stackoverflow.com/questions/4859292/how-to-get-a-random-value-from-dictionary-in-python
      self.edit_filter_mode = False
      self.filterimg = False     # apply selected_filters
      self.effectimg = False     # apply effects
      self.selected_filters = [] # the filters to apply
      self.grayscale = False
      self.blur = False          # blur filter on or off
      self.contour = False       # contour filter on or off
      self.detail = False        # detail filter on or off
      self.enhance = False       # edges enhance filter on or off
      self.enhance_more = False  # edges enhance more filter on or off
      self.emboss = False        # emboss filter on or off
      self.edges = False         # find edges filter on or off
      self.sharpen = False       # sharpen filter on or off
      self.smooth = False        # smooth filter on or off
      self.smooth_more = False   # smooth more filter on or off
      self.test = False
      self.keybindings = {}
      self.show_tb = True
      self.show_tb_diagtool = False
      self.show_tb_cmdtool = False
      self.show_tb_frametool = False
      self.start_as = 'normal'
      self.posx = 0
      self.posy = 0
      self.geometry = ''
      self.tb_widgets = []
      self.widgets = []
      self.widgets_on = False
      self.buttons_on = True # button override, will not hide with the widgets
      self.buttons = False
      self.fullscreen_mode = False
      self.zoom_on = False
      self.zoom_widgets_on = self.widgets_on
      self.is_GIF_file = False
      self.last_esc_key_press = None
      self.statusbar = None
      self.statusbar_labels = {}
      self.statusbar_thickness = 21
      self.center_image = False
      self.portrait = True
      self.landscape = True
      self.color = '#333333'
      # Picture Window
      self.picture_frame = None
      self.canvas = None
      # ToolBar
      self.toolbar = None
      self.folderbtn = None
      self.filebtn = None
      self.savebtn = None
      self.prevbtn = None
      self.luckybtn = None
      self.nextbtn = None
      self.showbtn = None
      self.repeatbtn = None
      self.randombtn = None
      self.shufflebtn = None
      self.resizebtn = None
      self.portraitbtn = None
      self.landscapebtn = None
      self.debugbtn = None
      # Frame Tool
      self.tb_frametool = None
      self.seekprevbtn = None
      self.seeknextbtn = None
      self.frame = 0
      self.no_frames = False
      # Command Tool
      self.tb_cmdtool = None
      self.commandbtn = None
      self.command_line = None
      # Diagnostic Tool
      self.tb_diagtool = None
      self.seperatorbtn = None
      self.tracebtn = None
      self.tracelbl = None
      self.bblvlvbtn = None
      self.bblvllbl = None
      self.menubar = None
      self.menufoo = None
      self.menu_on = False
      self.highquality = False
      self.lowquality = False
      self.thumbnail = False
      self.image_mode = False
      self.seperator = '-' * 60
      # movies
      self.playing = False
      self.supported_video_extensions = ['mpg','mp4','avi','flv','mov']
      self.supported_image_extensions = ['jpg','bmp','png','jpeg','gif','webp','webm','tiff','ico','ppm','b64']
      self.vidcap = None
      self.end_of_stream = False
      self.ffilestatusdisplaylbl = None
      self.alpha = 1.0
      self.transparency = False
      self.transparentcolor = '#123456'
      self.base64data = None
      self.perftime = 0
      self.images = []
      self.iimages = 0
      # https://www.codegrepper.com/code-examples/actionscript/python+get+current+user+windows
      self.current_user = os.getlogin()
      self.thumbsize = (200,200)
      self.desktop_mode = False
      self.show = True
      self.muted = False
      self.load_trunc = True
      self.module = ''
      self.module_name = ''
      self.module_ext = ''
      self.module_path = ''
      self.release_mode = False
      self.zoom = 1.0
      self.zoom_incdec = 0.01
      self.zoomed = False
      self.show_ui_error_messages = False # TODO: make error log file so I can log all issues with the files instead of stopping the show
      self.picturepos = 6 # Center = 0, Tile = 1 ("TileWallpaper" = 1), Stretch = 2, Fit = 6, Fill = 10
      self.logfile = '' # TODO: put in Log subdir, have to check if it exists then make if it doesn't and update path
      self.image_name = ''
      self.inspection_mode = False # for forensics, will not hide bad files if True
      self.transcoded = ''
      self.transcoded_savefilename = ''
      self.transcoded_saveprevfilename = ''
      self.verify = False # run extra verification checks like resize ratio tolerance
      self.use_canvas = False
      self.time_window = 1.0 # 1 second window
      self.logfile = "pillowtalk_" + str(self.time_stamp()) + "_log.txt" # txt so I can view in preview
      loginfo("Current User is",self.current_user)
      self.module = os.path.basename(sys.argv[0])
      loginfo("Module is",self.module)
      self.module_path = os.path.dirname(sys.argv[0])
      loginfo("Module Path is",self.module_path)
      self.module_name,self.module_ext = os.path.splitext(self.module)
      loginfo("Module Name is",self.module_name)
      loginfo("Module Extension is",self.module_ext)
      self.module_ext = self.module_ext.strip('. ')
      if self.module_ext == 'py':
        loginfo("Running in Console Mode")
      elif self.module_ext == 'pyw':
        loginfo("Running in Window Mode")
        release_mode = True
      else:
        logerror("I don't know what is going on here, this should not happen. You are on your own, Goodbye!");exit()
      self.last_esc_key_press = time.time_ns() / (10 ** 9)
      self.debug = self.show_tb_diagtool = debug
      self.transcoded_savefilename = '__acutiepy6de3f4da-f116-452b-87d3-a55c3078d189.jpg'
      self.transcoded_saveprevfilename = '__aTranscodedWallpaper.jpg'
      # init parent as late as possible right before we set geometry so we don't see the window pop from the default location to where we set it
      super().__init__()
      # TODO: need to initialize then pack, my functions have caused this to be a mess and display window then the final window, for now ill just set here and allow that bug to clean this up at a later date
      self.initialize_app()
      self.set_window_style(self.start_as, init=True)


    def initialize_app(self):
      # start tkinter, waiting until now as this is a starting gun and we need to place the window quickly or you see its default starting position and it is not very clean
      #self.set_window_style(self.start_as,init=True)
      self.tracelevel = StringVar()
      self.bblevel = StringVar()
      self.filenamepathlbltext = StringVar()
      self.active = tk.PhotoImage(data=self.smiley_face_button_image_gif_b64)
      self.inactive = tk.PhotoImage(data=self.straight_face_button_image_gif_b64)
      self.master.iconphoto(False, self.inactive)
      self.master.minsize(108,20) # (200,115) will resize image down to 64x64 if resize is True
      #self.master.wm_attributes('-type', 'dock')
      self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
      self.master.protocol("WM_SIZE", self.on_size)
      self.master.bind('<Configure>', self.on_window_resize)
      # https://stackoverflow.com/questions/46567324/tkinter-window-focus-loss-event
      self.master.bind("<FocusIn>", self.on_focus_in)
      self.master.bind("<FocusOut>", self.on_focus_out)

      # TODO: add command to change transparent color, when it was white it affected the images so that could get interesting
      self.master.wm_attributes("-transparentcolor", self.transparentcolor)
      self.master.wm_attributes('-alpha',self.alpha)
      self.master.title("Image Viewer")
      if self.debug is True: # start in BLACK
        self.master.configure(bg='#000000')
      else:
        self.master.configure(bg=self.color)
      self.initialize_window(show_pic_window=True)


    @trace(5)
    def on_focus_in(self, event):
      loginfo("Have Focus")
      self.master.iconphoto(False, self.active)


    @trace(5)
    def on_focus_out(self, event):
      loginfo("Lost Focus")
      self.master.iconphoto(False, self.inactive)


    def set_window_style(self,style,init=False):
      if style not in self.windows_geometries:
        logwarn("Geometry '"+str(style)+"' Not Found, defaulting to 'normal'")
        style = 'normal'
      if style == 'tool':
        # set widgets on for tool mode or its not tool mode
        self.posx = int(self.master.winfo_screenwidth() - 150)
        self.posy = int(self.master.winfo_screenheight() / 1.85)
        self.show_buttons()
        self.buttons_on = True
        if self.widgets_on is True:
          self.hide_widgets()
      elif style == 'widget':
        self.posx = int(self.master.winfo_screenwidth() - 150)
        self.posy = int(self.master.winfo_screenheight() / 5) # / 1.85
        self.hide_buttons()
        self.buttons_on = False
        if self.widgets_on is True:
          self.hide_widgets()
      elif style == 'compact':
        self.posx = 150
        self.posy = 100
        self.show_buttons()
        self.buttons_on = True
        if self.widgets_on is True:
          self.hide_widgets()
      elif style == 'normal':
        self.posx = 100
        self.posy = 50
        self.show_buttons()
        self.buttons_on = True
        if self.widgets_on is False:
          self.show_widgets()
      elif style == 'widescreen':
        self.posx = 100
        self.posy = 50
        self.hide_buttons()
        self.buttons_on = False
        if self.widgets_on is True:
          self.hide_widgets()
      else:
        logwarn("'"+str(style)+"' is not a valid style")
        return

      loginfo("Style:",style,", Width:",self.windows_geometries[style]['width'], \
                                        ", Height:",self.windows_geometries[style]['width'], \
                                        ", X:",self.posx,", Y:",self.posy)
      self.geometry = str(self.windows_geometries[style]['width']) + 'x' + \
                      str(self.windows_geometries[style]['height']) + '+' + \
                      str(self.posx) + '+' +  str(self.posy)
      loginfo("Setting Geometry To:",self.geometry)
      self.master.geometry(self.geometry)


    @trace(3)
    def initialize_window(self, show_pic_window=True):
      loginfo("Initializing Main Window")

      #self.master.bind("<Motion>", self.on_motion) # see mouse movement
      self.master.bind('<Button-1>', self.on_click) # left mouse click

      # TODO: menu bar needs to be updated with all the functionality (lots of busy work), DONE->needs to be addable and removable.
      self.initialize_menu_bar()
      self.initialize_toolbar(state=DISABLED)

      self.initialize_shortcuts(self.master)

      if show_pic_window is True:
        self.initialize_picture_frame(state=DISABLED,show=True)
        # TODO: status bar, show app states, playing, shuffled, image informaton etc.
        # TODO: thumbnail directory view and/or thumbnail carasel
        self.initialize_statusbar(show=self.resize)
        #self.initialize_carousel()

      if show_pic_window is True:
        if len(self.targets): # if targest are provided see if it's a path or file
          if self.canvas is not None:
            # DONE: findout what time frequency after takes, 60 is to fast to be seconds. A: it's milliseconds
            self.canvas.after(100, self.process_command_line_arguments)
      else:
        self.master.bind('<Return>', self.on_fullscreen)
        self.master.bind('<Escape>', self.on_windowed)

      if self.transparency is True:
        self.set_window_color(self.transparentcolor)
      else:
        self.set_window_color(self.color)

      if self.widgets_on is not True:
        self.hide_widgets()


    @trace(3)
    def show_buttons(self):
      if self.buttons is not True:
        self.leftbtn.pack(side=LEFT)
        self.rightbtn.pack(side=RIGHT)
        self.buttons = True


    @trace(3)
    def hide_buttons(self):
      if self.buttons is True:
        self.leftbtn.pack_forget()
        self.rightbtn.pack_forget()
        self.buttons = False


    @trace(3)
    def show_widgets(self):
      loginfo("Showing All Control Widgets")
      if self.menu_on is True:
        self.show_menu()
      self.show_toolbar()
      if self.resize is True:
        self.show_statusbar()
      #self.show_carousel()
      self.show_buttons()
      self.widgets_on = True


    @trace(3)
    def hide_widgets(self):
      loginfo("Hiding All Control Widgets")
      self.hide_menu()
      self.hide_toolbar()
      self.hide_statusbar()
      #self.hide_carousel()
      if self.buttons_on is False:
        self.hide_buttons()
      self.widgets_on = False


    @trace(3)
    def on_toggle_widgets(self,event):
        self.toggle_widgets()


    @trace(3)
    # Order is important, add according to pack order. Menu is independent as it isn't packed but toolbar, carousel and statusbar should be added in that order from top to bottom.
    def toggle_widgets(self,toggle=True,value=True):
      if toggle is False:
        self.widgets_on = value
      else:
        self.widgets_on = not self.widgets_on
      if self.widgets_on is True:
        self.show_widgets()
      else:
        self.hide_widgets()


    @trace(3)
    def initialize_menu_bar(self):
      loginfo("Initializing Menu")
      self.menfoo = BooleanVar(value=False)
      # Create Menu
      self.menubar = Menu(self.master,font=("times new roman",15,"normal"),activebackground="skyblue")
      loginfo("MenuBar",self.menubar)
      # Create Test Menu
      self.testmenu = Menu(self.menubar,font=("times new roman",12,"normal"),activebackground="skyblue",tearoff=0)
      self.testmenu.add_checkbutton(label="Foo",command=self.foo,variable=self.menfoo,onvalue=True,offvalue=False)
      self.menubar.add_cascade(label="Test", menu=self.testmenu)
      self.menfoo.set(True)
      loginfo("TestMenu",self.testmenu)
      # set menu in config here, mimick win32
      if self.menu_on is True and self.fullscreen_mode is False:
        self.show_menu()


    @trace(3)
    def hide_menu(self):
      loginfo("Hiding Menu")
      # Configuring empy menu
      if self.menufoo is None:
        self.menufoo = Menu(self.master)
      self.master.config(menu=self.menufoo)


    @trace(3)
    def show_menu(self):
      loginfo("Showing Menu")
      # Configuring menubar on root window
      if self.widgets_on is True:
        self.master.config(menu=self.menubar)


    @trace(3)
    def on_toggle_menu(self,event):
        self.toggle_menu()


    @trace(3)
    def toggle_menu(self,toggle=True,value=True):
      if toggle is False:
        self.menu_on = value
      else:
        self.menu_on = not self.menu_on
      if self.menu_on is True:
        self.show_menu()
      else:
        self.hide_menu()


    @trace(3)
    def initialize_picture_frame(self,state=None,show=False,pack_only=False):
      loginfo("Initializing Picture Window")
      if pack_only is False:
        # DONE: pri=0;sev=0; fix picture box alignment, it is under the tb_widgets and commandbar. was setting frame to self not master
        if self.debug is True: # highlight frame in WHITE
          self.picture_frame = Frame(self.master,bg="#D0D0D0")
        else: # start in BLACK
          self.picture_frame = Frame(self.master,bg=self.color)
        # https://pythonguides.com/python-tkinter-label/
        # https://stackoverflow.com/questions/18369936/how-to-open-pil-image-in-tkinter-on-canvas
        if self.use_canvas is False:
          if self.debug is True: # highlight label
            self.canvas = Label(self.picture_frame,justify=CENTER,bg="#00ff00")
          else: # start in BLACK
            self.canvas = Label(self.picture_frame,justify=CENTER,bg=self.color)
          self.canvas.pack()
          # TODO: do we need this ? re: self.canvas.place
          self.canvas.place(in_=self.picture_frame, relx=0.5, rely=0.5, anchor="center")# DONE: optionally add prev next image buttons to the picture frame
        else:
          if self.debug is True: # highlight
            self.canvas = Canvas(self.picture_frame, width=0, height=0, bg="#00ff00")
          else:
            self.canvas = Canvas(self.picture_frame, width=0, height=0, bg=self.color)
          self.canvas.pack(side = TOP)
          self.canvas.place(in_=self.picture_frame, relx=0.5, rely=0.5, anchor="center")
        # TODO: create images for these buttons to make them nice, maybe different ones implementing schemes with color etc.
        #leftbtnimg= PhotoImage(file='foo.gif')
        #rightbtnimg = PhotoImage(file='bar.gif')
        # https://stackoverflow.com/questions/44331618/tkinter-button-image-transparent-background
        self.leftbtn = Button(self.picture_frame, text="<", relief=GROOVE, command=self.prev_slide)
        #self.leftbtn.pack(side=LEFT)
        #self.leftbtn.config(image=leftbtnimg, background=self.color,foreground='w')
        self.leftbtn.config(background=self.color,foreground='#FFFFFF')
        self.rightbtn = Button(self.picture_frame, text=">", relief=GROOVE, command=self.next_slide)
        #self.rightbtn.pack(side=RIGHT)
        #self.rightbtn.config(image=rightbtnimg, background=self.color,foreground='w')
        self.rightbtn.config(background=self.color,foreground='#FFFFFF')
        if self.picture_frame not in self.widgets:
          self.initialize_picture_frame(pack_only=True)
        if self.picture_frame is not None:
          loginfo("Initializing Shortcuts")
          self.initialize_picture_shortcuts(self.picture_frame)
      if pack_only is True or show is True:
        if self.widgets_on is True or self.buttons_on is True:
          self.leftbtn.pack(side=LEFT)
          if state is not None: self.leftbtn['state'] = state
          self.rightbtn.pack(side=RIGHT)
          if state is not None: self.rightbtn['state'] = state
        self.picture_frame.pack(side=TOP, fill=BOTH, expand=YES)
        if self.picture_frame is not None:
          self.picture_frame.focus_set()


    @trace(3)
    def initialize_toolbar(self,state=None,show=False,pack_only=False):
      loginfo("Initializing Toolbar")
      if pack_only is False:
        # Create Toolbar
        if self.debug is True:
          self.toolbar = Frame(self.master,bg="#ff00ff")
        else:
          self.toolbar = Frame(self.master)
        self.folderbtn = Button(self.toolbar, text="Folder", relief=GROOVE, command=self.open_directory_dialog)
        self.folderbtn.pack(side=LEFT)

      if pack_only is False:
        self.filebtn = Button(self.toolbar, text="Media", relief=GROOVE, command=self.open_file_dialog)
        self.filebtn.pack(side=LEFT)

      if pack_only is False:
        self.savebtn = Button(self.toolbar, text="Save", relief=GROOVE, command=self.save_file_as_dialog)
        self.savebtn.pack(side=LEFT)
        if state is not None: self.savebtn['state'] = state

      if pack_only is False:
        self.prevbtn = Button(self.toolbar, text="[<]", relief=GROOVE, command=self.file_prev)
        self.prevbtn.pack(side=LEFT)
        if state is not None: self.prevbtn['state'] = state

      # TODO: scale toolbar like a web page, e.g. remove and add this button depending on size of window
      if pack_only is False:
        self.luckybtn = Button(self.toolbar, text="[<>]", relief=GROOVE, command=self.file_random)
        self.luckybtn.pack(side=LEFT)
        if state is not None: self.luckybtn['state'] = state

      if pack_only is False:
        self.nextbtn = Button(self.toolbar, text="[>]", relief=GROOVE, command=self.file_next)
        self.nextbtn.pack(side=LEFT)
        if state is not None: self.nextbtn['state'] = state

      if pack_only is False:
        self.showbtn = Button(self.toolbar, text="Start", relief=GROOVE, command=self.start_slideshow)
        self.showbtn.pack(side=LEFT)
        if state is not None: self.showbtn['state'] = state

      if pack_only is False:
        self.repeatbtn = Button(self.toolbar, text="Once", relief=GROOVE, command=self.toggle_repeat)
        self.repeatbtn.pack(side=LEFT)
        if state is not None: self.repeatbtn['state'] = state

      # TODO: fix backwards button text, this says A-Z when it is not in random mode (list order mode or a-z mode or ordered mode) and 'Rand' when in, should be other way around as the button should display the mode the you wish to select and go into. Other buttons do the same so vet all buttons, status will show the mode for clarity as I liked seeing the state and it seemed less confusing but I will be confusing others if I go this route so this is a better solution
      if pack_only is False:
        self.randombtn = Button(self.toolbar, text="A-Z", relief=GROOVE, command=self.toggle_random)
        self.randombtn.pack(side=LEFT)
        if state is not None: self.randombtn['state'] = state

      if pack_only is False:
        self.shufflebtn = Button(self.toolbar, text="Shuffle", relief=GROOVE, command=self.toggle_shuffle)
        self.shufflebtn.pack(side=LEFT)
        if state is not None: self.shufflebtn['state'] = state

      if pack_only is False:
        self.resizebtn = Button(self.toolbar, text="Resize", relief=GROOVE, command=self.toggle_resize)
        self.resizebtn.pack(side=LEFT)

      if pack_only is False:
        self.filterbtn = Button(self.toolbar, text="Raw", relief=GROOVE, command=self.toggle_filters)
        self.filterbtn.pack(side=LEFT)

      if pack_only is False:
        self.portraitbtn = Button(self.toolbar, text=" [*] ", relief=GROOVE, command=self.toggle_portrait)
        self.portraitbtn.pack(side=LEFT)
        self.portrait = True # False is [x]

      if pack_only is False:
        self.landscapebtn = Button(self.toolbar, text="[  *  ]", relief=GROOVE, command=self.toggle_landscape)
        self.landscapebtn.pack(side=LEFT)
        self.landscape = True # False is [  x  ]

      if pack_only is False:
        self.highqualitybtn = Button(self.toolbar, text="*", relief=GROOVE, command=self.toggle_highquality)
        self.highqualitybtn.pack(side=LEFT)
        self.highquality = False # True is [  $  ]

      if pack_only is False:
        self.lowqualitybtn = Button(self.toolbar, text="@", relief=GROOVE, command=self.toggle_lowquality)
        self.lowqualitybtn.pack(side=LEFT)
        self.lowquality = False # True is [  ~  ]

      if pack_only is False:
        self.imagemodebtn = Button(self.toolbar, text="I", relief=GROOVE, command=self.toggle_image_mode)
        self.imagemodebtn.pack(side=LEFT)

      if pack_only is False:
        self.desktopmodebtn = Button(self.toolbar, text="D", relief=GROOVE, command=self.toggle_desktop_mode)
        self.desktopmodebtn.pack(side=LEFT)

      if pack_only is False:
        self.debugbtn = Button(self.toolbar, text="(i)", relief=GROOVE, command=self.toggle_debug)
        self.debugbtn.pack(side=LEFT)

      if pack_only is False:
        self.initialize_frame_tool(self.toolbar)
        #self.initialize_diagnostics_tool(self.toolbar)
        self.initialize_command_tool(self.toolbar)

      if pack_only is False:
        if self.toolbar not in self.widgets:
          if self.fullscreen_mode is False:
            self.initialize_toolbar(pack_only=True)

      if pack_only is True or show is True:
        self.toolbar.pack(side=TOP, fill=X)
        if self.toolbar not in self.widgets:
          self.widgets.append(self.toolbar)


    @trace(3)
    def hide_toolbar(self):
      loginfo("Hiding Tool Bar")
      self.toggle_command_tool(toggle=False,value=False)
      self.toolbar.pack_forget()
      if self.toolbar in self.widgets:
        self.widgets.remove(self.toolbar)


    @trace(3)
    def show_toolbar(self):
      loginfo("Showing Tool Bar")
      if self.picture_frame is not None:
        self.picture_frame.pack_forget()
      self.initialize_toolbar(pack_only=True)
      if self.toolbar not in self.widgets:
        self.widgets.append(self.toolbar)
      if self.picture_frame is not None:
        self.initialize_picture_frame(pack_only=True)
        # TODO: Should I unbind before rebinding? Look into bindings
        self.initialize_picture_shortcuts(self.picture_frame)
        self.picture_frame.focus_set()


    @trace(3)
    def initialize_frame_tool(self,container,text='0/0',state=None,show=False,pack_only=False):
      # pages
      loginfo("Initializing Frame Tool")
      if pack_only is False:
        if self.debug is True: # highlight Frame in RED
          self.tb_frametool = Frame(container,bg='#555555')
        else:
          self.tb_frametool = Frame(container, bg=self.color)
        self.num_page=0
        self.framecntr = StringVar()
        self.framerate = StringVar()

      if pack_only is False:
        Label(self.tb_frametool, text="Frame").pack(side=LEFT)
        Label(self.tb_frametool, textvariable=self.framecntr).pack(side=LEFT)
        self.framecntr.set(text)

       # TODO: add seperate loop for frames so these can be set seperately

      if pack_only is False:
        self.playbtn = Button(self.tb_frametool, text=">", relief=GROOVE, command=self.play_pause)
        self.playbtn.pack(side=LEFT)
        if state is not None: self.seekprevbtn['state'] = state

      if pack_only is False:
        self.seekhomebtn = Button(self.tb_frametool, text="<<", relief=GROOVE, command=self.seek_home)
        self.seekhomebtn.pack(side=LEFT)
        if state is not None: self.seekhomebtn['state'] = state

      if pack_only is False:
        self.seekprevbtn = Button(self.tb_frametool, text="<", relief=GROOVE, command=self.frame_seek_prev)
        self.seekprevbtn.pack(side=LEFT)
        if state is not None: self.seekprevbtn['state'] = state

      if pack_only is False:
        self.seeknextbtn = Button(self.tb_frametool, text=">", relief=GROOVE, command=self.frame_seek_next)
        self.seeknextbtn.pack(side=LEFT)
        if state is not None: self.seeknextbtn['state'] = state

      if pack_only is False:
        self.seekendbtn = Button(self.tb_frametool, text=">>", relief=GROOVE, command=self.seek_end)
        self.seekendbtn.pack(side=LEFT)
        if state is not None: self.seekendbtn['state'] = state

      if pack_only is False:
        Label(self.tb_frametool, text="fps").pack(side=LEFT)
        Label(self.tb_frametool, textvariable=self.framerate).pack(side=LEFT)
        self.framerate.set(text)

      if pack_only is False:
        if self.show_tb_frametool is True:
          initialize_frame_tool(self.toolbar,pack_only=True)

      if pack_only is True or show is True:
        self.tb_frametool.pack(side=LEFT, fill=X)
        if self.tb_frametool not in self.tb_widgets:
          self.tb_widgets.append(self.tb_frametool)


    @trace(3)
    def initialize_command_tool(self,container,setfocus=False,show=False,pack_only=False):
      """ Initialize the command bar """
      loginfo("Initializing Command Tool")
      # command bar (framed to bundle it as a whole control)
      if pack_only is False:
        self.cmd = StringVar()
        if self.debug is True: # highlight Frame in RED
          self.tb_cmdtool = Frame(container,bg='#990000')
        else:
          self.tb_cmdtool = Frame(container, bg=self.color)
        #self.cmd.set('filter blackvelvetpainting') # quick way to test a command
        # TODO: pri=3;sev=3; add after callback for sending enter button on command bar for test but may be useful if command line arguments are used to specify commands
        # https://www.tutorialspoint.com/python/tk_entry.htm
        # https://www.geeksforgeeks.org/python-tkinter-entry-widget/
        self.command_line = Entry(self.tb_cmdtool, relief=SOLID,textvariable=self.cmd,font=("times new roman",15,"normal"))
        self.commandbtn = Button(self.tb_cmdtool, text="CMD::", relief=GROOVE, command=self.process_command)
        self.commandbtn.pack(side=LEFT)
        # https://www.python-course.eu/tkinter_events_binds.php
        self.command_line.bind("<Return>", self.on_process_command)
        self.command_line.bind("<Up>", self.on_next_cmd_history)    # navigate history
        self.command_line.bind("<Down>", self.on_prev_cmd_history)  # navigate history

      if pack_only is False:
        Button(self.tb_cmdtool, text="<", relief=GROOVE, command=self.prev_cmd_history).pack(side=LEFT)
        Button(self.tb_cmdtool, text=">", relief=GROOVE, command=self.next_cmd_history).pack(side=RIGHT)
        self.command_line.pack(side=TOP,fill=X)

      if pack_only is False:
        if self.show_tb_cmdtool is True:
          self.initialize_command_tool(self.toolbar,pack_only=True)

      if pack_only is True or show is True:
        self.tb_cmdtool.pack(side=TOP, fill=X)
        if self.tb_cmdtool not in self.tb_widgets:
          self.tb_widgets.append(self.tb_cmdtool)
        if setfocus is True:
          self.command_line.focus_set()


    @trace(3)
    def initialize_diagnostics_tool(self,container,show=False,pack_only=False):
      # DONE: add clearscreen (system(cls))
      loginfo("Initializing Diagonstics Tool")
      if pack_only is False:
        if self.debug is True: # highlight Frame in RED
          self.tb_diagtool = Frame(container,bg='#0000ff')
        else:
          self.tb_diagtool = Frame(container, bg=self.color)
        # self test button
        self.testbtn = Button(self.tb_diagtool, text="Test", relief=GROOVE, command=self.perform_self_test)
        self.testbtn.pack(side=LEFT)
      if pack_only is False:
        self.clsbtn = Button(self.tb_diagtool, text="cls", relief=GROOVE, command=self.clearscreen)
        self.clsbtn.pack(side=LEFT)
      # seperator button
      if pack_only is False:
        self.seperatorbtn = Button(self.tb_diagtool, text="---", relief=GROOVE, command=self.insert_seperator)
        self.seperatorbtn.pack(side=LEFT)
      # trace level button and label
      if pack_only is False:
        self.tracebtn = Button(self.tb_diagtool, text=">>>", relief=GROOVE, command=self.cycle_trace_verbosity)
        self.tracebtn.pack(side=LEFT)
      if pack_only is False:
        self.tracelbl = Label(self.tb_diagtool, textvariable=self.tracelevel)
        self.tracelbl.pack(side=LEFT)
        self.tracelevel.set(str(gettracelevel()))
      # trace level button and label
      if pack_only is False:
        self.bblvlvbtn = Button(self.tb_diagtool, text="trace lvl", relief=GROOVE, command=self.cycle_bb_verbosity)
        self.bblvlvbtn.pack(side=LEFT)
      if pack_only is False:
        self.bblvllbl = Label(self.tb_diagtool, textvariable=self.bblevel)
        self.bblvllbl.pack(side=LEFT)
        self.bblevel.set(getlevel())
      #if pack_only is False:
        #if self.show_tb_diagtool is True:
          #self.initialize_diagnostics_tool(self.toolbar,pack_only=True)
      if pack_only is True or show is True:
        self.tb_diagtool.pack(side=LEFT, fill=X)
        if self.tb_diagtool not in self.tb_widgets:
          self.tb_widgets.append(self.tb_diagtool)


    @trace(3)
    def initialize_carousel(self,show=False,pack_only=False):
      # https://pythonbasics.org/tkinter-image/ has placing images i.e. img.place(x=0,y=0)
      # TODO: Carousel UNDERCONSTRUCTION: for each thumbnail add a label an put the thumnail in it. to rotate just forget and repack starting from the index that should be leftmost
      # TODO: add buttons to either side of the carousel to go left or right, carousel will stop at begining and end of thumnails or continuous loop
      loginfo("Initializing Carousel")
      if pack_only is False:
        if self.debug is True: # highlight Frame in RED
          self.carousel = Frame(self.master,bg='#ff0000')
        else:
          self.carousel = Frame(self.master, bg=self.color)
        label = Label(self.carousel , text="Carousel")
        Button(self.carousel, text="<", relief=GROOVE, command=self.prev_cmd_history).pack(side=LEFT)
        Button(self.carousel, text=">", relief=GROOVE, command=self.next_cmd_history).pack(side=RIGHT)
        label.pack(side=LEFT)
      if pack_only is True or show is True:
        loginfo("Showing Carousel")
        self.carousel.pack(side=BOTTOM, fill=X)
        self.widgets.append(self.carousel)


    @trace(3)
    def hide_carousel(self):
      if self.carousel in self.widgets:
        loginfo("Hiding Carousel")
        self.carousel.pack_forget()
        self.widgets.remove(self.carousel)


    @trace(3)
    def show_carousel(self):
      if self.carousel not in self.widgets:
        loginfo("Showing Carousel")
        self.initialize_carousel(pack_only=True)


    @trace(3)
    def initialize_statusbar(self,show=False,pack_only=False):
      loginfo("Initializing Status Bar")
      if pack_only is False:
        if self.debug is True: # highlight Frame in RED
          self.statusbar = Frame(self.master, height=self.statusbar_thickness, bg='#0000ff')
        else:
          self.statusbar = Frame(self.master, height=self.statusbar_thickness)
        #self.add_statusbar_label(self.statusbar)
        self.statusinfolbl = Label(self.statusbar)
        self.statusinfolbl.pack(side=LEFT)
        self.stauserrorlbl = Label(self.statusbar)
        self.stauserrorlbl.pack(side=RIGHT)
      if pack_only is True or show is True:
        self.statusbar.pack(side=BOTTOM, fill=X, anchor=S)
        if self.statusbar not in self.widgets:
          self.widgets.append(self.statusbar)


    @trace(3)
    def hide_statusbar(self):
      if self.statusbar in self.widgets:
        loginfo("Hiding Status Bar")
        self.statusbar.pack_forget()
        self.widgets.remove(self.statusbar)
      else:
        loginfo("WTF Man!")


    @trace(3)
    def show_statusbar(self):
      if self.statusbar not in self.widgets:
        loginfo("Showing Status Bar")
        self.initialize_statusbar(pack_only=True)


    @trace(3)
    def add_statusbar_label(self,container):
      loginfo("Adding Status Bar Label")
      label = Label(container, text="Status")
      self.statusbar_labels["status"] = label
      label.pack(side=LEFT)


    @trace(3)
    def initialize_shortcuts(self,widget):
      """ Initialize shortcuts for application """
      # https://wingware.com/doc/custom/key-names
      # https://www.pythontutorial.net/tkinter/tkinter-event-binding/
      # widget.bind(event, handler, add=None) E.g. root.bind('<Return>', handler)
      # *widget.bind_class(class, event, handler, add=None) E.g. root.bind_class('Entry', '<Control-V>', paste)
      # widget.unbind(event) E.g. btn.unbind('<Return>')
      # * needs confirmation, may contain errors; best guess

      # move window
      # https://stackoverflow.com/questions/16082243/how-to-bind-ctrl-in-python-tkinter
      # https://www.pythontutorial.net/tkinter/tkinter-event-binding/
      widget.bind('<Alt-Up>', self.on_up, add=None)                  # add='+' will add vs replace the binding
      widget.bind('<Alt-Down>', self.on_down)              #
      widget.bind('<Alt-Left>', self.on_left)              #
      widget.bind('<Alt-Right>', self.on_right)            #
      widget.bind('<Control-Up>', self.on_up_fast)        #
      widget.bind('<Control-Down>', self.on_down_fast)    #
      widget.bind('<Control-Left>', self.on_left_fast)    #
      widget.bind('<Control-Right>', self.on_right_fast)  #
      widget.bind('<Alt-c>', self.on_center)               #

      widget.bind('<F12>', self.on_toggle_debug)          # toggle debug and diagnostics tool
      widget.bind('<F11>', self.on_toggle_test_flag)      # toggle test? is this really a toggle?
      widget.bind('<F10>', self.on_set_wallpaper)         # this is used by the system or something else and it toggles on/off all F keys. F keys toggle on when other keys are presssed

      widget.bind('<F1>', self.on_help)                   # display help
      widget.bind('<F2>', self.on_toggle_widgets)         # toggle all widgets except picture on and off for full screen on secondary monitor until I figure out how to do this for real, secondary full screen will be toggling widgets off so they don't obstruct view and maimizing the screen. The top window bar is still there but the bad video alignment almost completely obscures it on my LCD TV.
      widget.bind('<F3>', self.on_toggle_zoom)            # zoom zoom
      widget.bind('<F4>', self.on_crop)                   # crop
      # TODO: change F5 to refresh and add a command to draw image info
      widget.bind('<F5>', self.on_draw_image_info)        # draw image info onto the image


      # DONE: + - zoom in out
      # **** TODO: shift values for transparency and un-shifted for zoom in/out
      widget.bind('=', self.on_zoom_in)       # increase entire window transparency
      widget.bind('-', self.on_zoom_out)      # decrease entire window transparency

      widget.bind('<Shift-plus>', self.on_increase_alpha)         # increase entire window transparency
      widget.bind('<Shift-underscore>', self.on_decrease_alpha)   # decrease entire window transparency


      widget.bind('<F6>', self.on_slate)
      widget.bind('<F7>', self.on_white)
      widget.bind('<F8>', self.on_black)
      widget.bind('<F9>', self.on_transparent)

      # https://tkinter-discuss.python.narkive.com/6048wtTR/bind-alt-1-5-not-working
      # development keys for generating images before i move them to more permanent locations
      widget.bind('<Alt-KeyPress-1>', self.on_generate_image)
      widget.bind('<Alt-KeyPress-2>', self.on_generate_image)
      widget.bind('<Alt-KeyPress-3>', self.on_generate_image)
      widget.bind('<Alt-KeyPress-4>', self.on_generate_image)
      widget.bind('<Alt-KeyPress-5>', self.on_generate_image)
      widget.bind('<Alt-KeyPress-6>', self.on_generate_image)
      widget.bind('<Alt-KeyPress-7>', self.on_generate_image)
      widget.bind('<Alt-KeyPress-8>', self.on_generate_image)
      widget.bind('<Alt-KeyPress-9>', self.on_generate_image)
      widget.bind('<Alt-KeyPress-0>', self.on_generate_image)


      widget.bind('<Alt-F1>', self.on_foo) # iconify
      widget.bind('<Alt-F2>', self.on_bar) # minimize
      widget.bind('<Alt-F3>', self.on_foo) # maximze
      #widget.bind('<Alt-F4>', self.bar)   # close, windows uses this key already so i'm incorporating it in

      widget.bind('<Alt-F5>', self.on_tool)
      widget.bind('<Alt-F6>', self.on_widget)
      widget.bind('<Alt-F7>', self.on_compact)
      widget.bind('<Alt-F8>', self.on_normal)
      widget.bind('<Alt-F9>', self.on_widescreen)
      widget.bind('<Alt-F10>', self.on_foo) # if its not set F10 will handle it and we don't want that
      widget.bind('<Alt-F11>', self.on_foo) # if its not set F11 will handle it and we don't want that
      widget.bind('<Alt-F12>', self.on_foo) # if its not set F12 will handle it and we don't want that

      widget.bind('<Shift-F2>', self.on_play_pause)
      pass


    @trace(3)
    def initialize_picture_shortcuts(self,widget):
      """ Initialize shortcuts for the picture window """
      loginfo(f"Setting Keyboard Shortcuts. [{self}, {widget}]")
      # TODO: sort this out, the order is a little mismatched with comments
      # navigation
      widget.bind('<Up>', self.on_increase_interval)      # smaller increment faster slides
      widget.bind('<Down>', self.on_decrease_interval)    # larger increment slows slides
      widget.bind('<Left>', self.on_prev_slide)           # display previous image
      widget.bind('<Right>', self.on_next_slide)          # display next image
      # slides
      widget.bind('<space>', self.on_space)               # start stop slides
      widget.bind('<Home>', self.on_home)                 # stop and go back to the begining
      widget.bind('<End>', self.on_end)                   # stop and go to the end
      widget.bind('<Prior>', self.on_page_up)             # TBD, go forward one directory
      widget.bind('<Next>', self.on_page_down)            # TBD, go back one directory
      widget.bind('<Escape>', self.on_windowed)           # TBD, returned to the windowed state and remove fullscreen mode
      #widget.bind('<Foo>', self.on_foo)                  # Template
       # TENATIVE FIX: Sometimes the letter key shortcuts don't work but the arrow and F keys do. letter key shortcuts failed until I put set focus after pack but when I changed back it still worked. FIX: seperated into two functions to bind to half to main window and half to picture. So far no fails but this is not a solid fix.
      # Options
      # ----------------------------------- quick filters -------------------------------------------
      widget.bind('v', self.on_toggle_privacy)            # toggle image privacy and security (100% blur) mode
      widget.bind('y', self.on_toggle_grayscale)          # toggle grayscale mode
      # ----------------------------------- quick filters -------------------------------------------
      widget.bind('b', self.on_toggle_blur)               # toggle blur
      widget.bind('e', self.on_toggle_emboss)             # toggle emboss
      widget.bind('c', self.on_toggle_contour)            # toggle contour
      widget.bind('i', self.on_toggle_filters)            # toggle selected_filters
      widget.bind('h', self.on_toggle_enhance)            # toggle edge enhance
      widget.bind('p', self.on_toggle_sharpen)            # toggle sharpen
      widget.bind('m', self.on_toggle_smooth)             # toggle smooth
      widget.bind('d', self.on_toggle_detail)             # toggle detail
      widget.bind('g', self.on_toggle_edges)              # toggle find edges
      # --------------------------------------- filters ---------------------------------------------
      widget.bind('t', self.on_toggle_thumbnail)          # toggle thumbnail size
      widget.bind('n', self.on_new_filter)                # generate random new filter combo
      widget.bind('a', self.on_new_aggregate_filter)      # generate random new filter that aggregates or (m)ultiplies generations
      widget.bind('x', self.on_clear_selected_filters)    # turn all selected_filters of except privacy and security image blur
      # --------------------------------------- slides ----------------------------------------------
      widget.bind('f', self.on_fullscreen)                # put app into fullsreen mode
      widget.bind('r', self.on_file_random)               # display random image
      widget.bind('l', self.on_repeat)                    # repeat/loop slide show
      widget.bind('o', self.on_img_orig)                  # resize displayed images to original size
      widget.bind('w', self.on_img_resize)                # resize displayed images to window size
      widget.bind('s', self.on_toggle_resize)             # toggle resizing displayed images from origional size to window size
      widget.bind('z', self.on_toggle_random)             # toggle random/sequential
      # ---------------------------------------- tools ----------------------------------------------
      # DONE: re-add GIF frame inspection functionality but this time for GIF only
      widget.bind('[', self.on_toggle_frames_tool)        # toggle GIF frames tool
      widget.bind('.', self.on_toggle_command_tool)       # toggle command tool
      widget.bind('u', self.on_toggle_menu)               # toggle menu

      widget.bind('j', self.toggle_desktop_mode)          # jack the desktop! display also using desktop background
      #widget.bind('<Control-+>', self.on_foo)            # zoom in
      widget.bind('<Control-=>', self.on_foo)             # zoom in
      widget.bind('<Control-minus>', self.on_bar)         # zoom out
      #widget.bind('<Control-_>', self.on_foo)            # zoom out
      widget.bind('q', self.on_toggle_shuffle)            # shuffle
      widget.bind('k', self.on_toggle_effects)            # toggle effects


    @trace(3)
    def on_set_wallpaper(self,event):
      if self.desktop_mode is True:
        loginfo("Update Saved Desktop Wallpaper")
        self.update_saved_desktop_wallpaper()
      else:
        loginfo("Set Desktop Wallpaper")
        self.set_wallpaper_from_image()


    @trace(3)
    def set_wallpaper_from_image(self,image=None,print_info=True):
      # SetSysColor (winuser.h)
      # https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setsyscolors?redirectedfrom=MSDN
      # https://stackoverflow.com/questions/847850/cross-platform-way-of-getting-temp-directory-in-python
      # DONE: if slide show is running on desktop overwrite the saved desktop image to restore and set
      loginfo(tempfile.gettempdir()) # prints the current temporary directory
      #filename=str(uuid.uuid4()).strip(' ')
      # will need to do some mode checking and conversions
      if image is None:
        image = self.filtimg
      if image is not None:

        transcoded = ntpath.join(tempfile.gettempdir(),self.transcoded_savefilename)
        loginfo("Transcoded File:",transcoded)
        if image.mode != 'RGB':
          loginfo("Converting Image to RGB")
          image = self.filtimg.convert('RGB')
        self.print_image_info(image,
                             show_file=False,
                             test_images=False,
                             check_format_modes=False,
                             check_palette=False)
        #image = self.get_resized_img_fit(image,size=(self.master.winfo_screenwidth(),self.master.winfo_screenheight()))
        loginfo("Save 2 & Set Wallpaper from",transcoded)
        image.save(transcoded)
        self.set_wallpaper_from_file(transcoded)
        # https://stackoverflow.com/questions/50806334/tkinter-keep-from-moving-focus-to-window
        self.picture_frame.focus_set()


    @trace(3)
    # This code is based on the following two links
    # http://mail.python.org/pipermail/python-win32/2005-January/002893.html
    # http://code.activestate.com/recipes/435877-change-the-wallpaper-under-windows/
    def set_wallpaper_from_file(self,filepathname=None):
      # DONE: make temp file from current image filtered (sized?) an all and put that as the wallpaper instead of the original file cause that is what we do this for baby!
      # TODO: add minimize to systray and when minimized the program will run using the computers desktop wallpaper to display the images
      # TODO: add Fill, Fit, Stretch, Tile, Center options to the desktop wallpaper display. Do these the same as the system.
      # TODO: add option to fit if greater than and don't resize on less than. I.g. shrink but don't expand. Good scanning mode.
      # https://www.blog.pythonlibrary.org/2014/10/22/pywin32-how-to-set-desktop-background/
      # -- or --
      # https://stackoverflow.com/questions/40574622/how-do-i-set-the-desktop-background-in-python-windows # winner winner chicken dinner
      if os.path.isfile(filepathname) is True: # DONE: need better way of determining if this is a file
        try:
          if filepathname is None:
            file = ntpath.join(self.root_directory,self.sources[self.isources])
          else:
            file = filepathname
          loginfo("Setting Wallpaper from", file)
          self.win32_set_wallpaper(file)
        except Exception as e:
          exception(e)


    @trace(3)
    def win32_set_wallpaper(self,file):
      SPI_SETDESKWALLPAPER  = 0x0014
      SPIF_UPDATEINIFILE    = 0x0001
      SPIF_SENDWININICHANGE = 0x0002
      # https://docs.python.org/3/library/ctypes.html
      user32 = ctypes.WinDLL('user32')
      SystemParametersInfo = user32.SystemParametersInfoW
      SystemParametersInfo.argtypes = ctypes.c_uint,ctypes.c_uint,ctypes.c_void_p,ctypes.c_uint
      SystemParametersInfo.restype = wintypes.BOOL
      # https://referencesource.microsoft.com/System/compmod/microsoft/win32/NativeMethods.cs.html#https://referencesource.microsoft.com/System/compmod/microsoft/win32/NativeMethods.cs.html,50f01645c4a3ac6b,references
      retval = SystemParametersInfo(SPI_SETDESKWALLPAPER, 0, file, SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE)
      if retval <= 0:
        logwarn("Failed to set desktop background with current image")


    @trace(3)
    def update_saved_desktop_wallpaper(self):
      curr = ntpath.join(tempfile.gettempdir(),self.transcoded_savefilename)
      save = ntpath.join(tempfile.gettempdir(),self.transcoded_saveprevfilename)
      loginfo("Save", curr,"to",save)
      shutil.copyfile(curr, save)


    @trace(3)
    def save_desktop_wallpaper(self):
      ''' Save the current desktop wallpaper in registry to cached wallpaper that is restored when desktop viewing is over. This will default to Windows cached wallpaper if that is not a valid path. '''
      try:
        key = winreg.OpenKey( winreg.HKEY_CURRENT_USER, r'Control Panel\Desktop', 0,  access=winreg.KEY_READ)
        transcoded,stype = winreg.QueryValueEx(key, "Wallpaper")
        loginfo("Wallpaper is",transcoded)
        loginfoanddie(transcoded)
        key.Close()
        if os.path.isfile(transcoded) is False:
          loginfo("Failed to get Registry cached wallpaper")
          # DONE: this path to the transcoded wallpaper is only if set by windows, what i set doesn't end up here so it is private to windows, not sure what the best solution for this is yet. Repro; F10 set wallpaper, jack then un-jack the desktop. Expected; my set wallpaper is restored. Result; last windows set wallpaper is restored. HKEY_CURRENT_USER\Control Panel\Desktop <Wallpaper>, also see HKEY_CURRENT_USER\Control Panel\Colors <background>
          transcoded = "C:\\Users\\" + str(self.current_user) + "\\AppData\Roaming\\Microsoft\\Windows\\Themes\\TranscodedWallpaper.jpg"
        if os.path.isfile(transcoded) is False:
          loginfo("Failed to get Windows cached wallpaper")
        save = ntpath.join(tempfile.gettempdir(),self.transcoded_saveprevfilename)
        loginfo("Save", transcoded, "to", save)
        # overwrite the cached wallpaper that is restored when not in desktop mode
        shutil.copyfile(transcoded, save)
      except Exception as e:
        exception(e)


    @trace(3)
    def restore_desktop_wallpaper(self):
      ''' Restore cached wallpaper to the desktop '''
      saved = ntpath.join(tempfile.gettempdir(),self.transcoded_saveprevfilename)
      loginfo("Restore", saved)
      self.set_wallpaper_from_file(saved)
      transcoded = ntpath.join(tempfile.gettempdir(),self.transcoded_savefilename)
      if os.path.exists(transcoded) is True: os.remove(transcoded)


    @trace(3)
    def image_todo_list():
      # https://pillow.readthedocs.io/en/5.1.x/reference/Image.html
      # https://pillow.readthedocs.io/en/stable/reference/Image.html
      # TODO: do a mode that matches the background color with the picture by sampling the predominant or background color
      # TODO: skip unloadable images and go to next image without displaying the failure image (user mode vs developer [devmode])
      # ------
      # Image.copy(), Image.crop(), Image.draft(), Image.filter(), Image.getbands(), Image.getbbox(), Image.getcolors(),
      # Image.getdata(), Image.getextreme(), Image.getpallete(), Image.getpixel(), Image.histogram(), Image.offset(),
      # Image.paste(), Image.point(), Image.putalpha(), Image.putdata, Image.putpallete, Image.putpixel, Image.quantize(),
      # Image.resize(), Image.remap_pallete(), Image.rotate(), Image.save(), Image.seek(), Image.show(), Image.getchannel(),
      # Image.tell(), Image.thumbnail(), Image.tobitmap(), Image.tobyes(), Image.tostring(), Image.transform(), Image.transpose(),
      # Image.verify(), Image.fromstring(), Image.close()
      # --------
      # TODO: use Image.getbbox() then Image.crop() to get automated square for icon output.
      # --------
      # Image.getcolors() # make absolutely sure the alpha mask is not a picture color by checking this on each picture and setting the mask to a value that is not one of these color in a mask variable that is set to the alpha mask
      # -------
      # Image.getdata() # get pixel data, image manipulation
      # ------
      # ImageDraw # drawing
      # ImageColor # https://hhsprings.bitbucket.io/docs/programming/examples/python/PIL/ImageColor.html
      # ------
      # Image.rotate() # standard stuff
      # ------
      # Image.split() # fun
      # ------
      # Image.getchannel() # more fun
      # ------
      # Image.seek(), Image.tell() # can I get these to work?
      # -----
      # PIL.Image.new(), PIL.Image.fromarray(), PIL.Image.frombytes(), PIL.Image.fromstring(), PIL.Image.frombuffer() # create images
      # ------
      # Image.tobitmap(),Image.tobytes(), Image.tostring() # see what real images look like converted to reverse engineer image creation
      # ------
      # Image.transform(), Image.transpose() # i support trans issues
      # ------
      # Image.verify(), better option then reading with truncated flag on?
      # ------
      # PIL.Image.alpha_composite(),PIL.Image.blend(),PIL.Image.composite(),PIL.Image.eval(),PIL.Image.merge() # i like blending
      # -----
      pass


    @trace(3)
    def get_resource_image(self):
      # for when we can't display and image for instance, due to privacy setting, we display this so something is displayed in it's place
      # Python3 needs to use .encode and .decode('utf8') otherwise same as ver 2
      # https://docs.python.org/3/library/base64.html
      # https://www.geeksforgeeks.org/base64-b64decode-in-python/
      jpg_bytes = base64.b64decode(self.false_2061132_1280_png_b64.encode())
      # https://docs.python.org/3/library/io.html
      io_bytes = io.BytesIO(jpg_bytes) # TODO: lookup exactly what this does, up till now i've only glanced
      return Image.open(io_bytes)


    @trace(3)
    def on_crop(self,event):
      self.crop()


    @trace(3)
    def crop(self,print_info=True):
      # https://pillow.readthedocs.io/en/5.1.x/reference/Image.html
      loginfo("Cropping Image")
      box = self.rawimg.getbbox()
      print("Box",box)
      cropimg = self.rawimg.crop(box)
      self.rawimg = cropimg.copy()
      if print_info is True: self.print_image_info(self.rawimg,
                                                   show_file=False,
                                                   test_images=False,
                                                   check_format_modes=False,
                                                   check_palette=False)
      self.display()
      if self.toolbar is not None: self.savebtn['state'] = NORMAL
      self.images.append(cropimg)


    @trace(3)
    def on_generate_image(self,event):
      loginfo("Event",event)
      self.generate_image(event.char)


    @trace(3)
    # development method for playing with different image generation methods
    def generate_image(self,gen_program='1',print_info=True):
      self.close_images()
      image = None
      if gen_program == '1':
        self.image_name = "Generated Image using Numpy Ones 40x30*150"
        # generate image
        #array = np.ones((40,40))*150 # gray square
        #array = np.zeros((40,40))*150 # black square
        # from numpy array
        array = np.random.random((300, 300))
        loginfo(array)
        image = Image.fromarray(array)
        #image.save('newtest.tiff')
      elif gen_program == '2':
        color = 'lavender'
        # https://pillow.readthedocs.io/en/5.1.x/reference/Image.html
        # https://www.programcreek.com/python/example/14029/PIL.Image.new
        # https://www.programcreek.com/python/example/92040/PIL.ImageStat.Stat
        # https://hhsprings.bitbucket.io/docs/programming/examples/python/PIL/ImageColor.html
        image = PIL.Image.new('RGB', (600,600),color=ImageColor.getrgb(color))
        self.image_name = "Generated Image using PIL Image New RGB 600_600"
        self.draw_image_info(image=image,show=False,color=color,filename=self.image_name)
      elif gen_program == '3':
        width,height = (1366,768)
        self.image_name = "Generated Mandelbrot Fractal Image "+str(width)+"_"+str(height)
        image = self.generate_mandelbrot_fractal_upd(width,height)
      elif gen_program == '4':
        width,height = (1366,768)
        self.image_name = "Generated Julia Fractal Image "+str(width)+"_"+str(height)
        image = self.generate_julia_fractal(width,height)
      elif gen_program == '5':
        # https://www.reddit.com/r/django/comments/30ndh9/pil_getcolors_and_getpalette_trying_to_get_rgb/
        # https://pillow.readthedocs.io/en/stable/_modules/PIL/Image.html#effect_mandelbrot
        # ****** TODO: blend, composite, merge, effect_mandelbrot, effect_noise, linear_gradient, radial_gradient
        image = Image.effect_mandelbrot((800,600),(-2.0,-1.5,1.0,1.5),100)
        #image = Image.effect_noise((800,600),100)
        #image = Image.linear_gradient('L')
        image = Image.radial_gradient('L')
      else:
        return
      self.rawimg = image.copy()
      if self.showfile is True:
        print(self.image_name)
      if self.privacy is True:
          self.master.title("Viewing in Privacy Mode")
      else:
        self.master.title("Viewing  " + self.image_name)
      if self.toolbar is not None: self.savebtn['state'] = NORMAL
      self.images.append(image)
      self.iimages = len(self.images) - 1
      self.image_mode = True
      self.display()


    def generate_julia_fractal(self,imgx,imgy):
      # Julia fractal
      # FB - 201003151
      from PIL import Image
      import random
      # drawing area (xa < xb and ya < yb)
      xa = -2.0
      xb = 1.0
      ya = -1.5
      yb = 1.5
      maxIt = 1024 # iterations
      image = Image.new("RGB", (imgx, imgy))
      # Julia set to draw
      c = complex(random.random() * 2.0 - 1.0, random.random() - 0.5)

      for y in range(imgy):
        zy = y * (yb - ya) / (imgy - 1)  + ya
        for x in range(imgx):
          zx = x * (xb - xa) / (imgx - 1) + xa
          z = complex(zx, zy)
          for i in range(maxIt):
              if abs(z) > 2.0: break
              z = z * z + c
          r = i % 4 * 64
          g = i % 8 * 32
          b = i % 16 * 16
          image.putpixel((x, y), b * 65536 + g * 256 + r)

      return image


    def generate_mandelbrot_fractal_upd(self,imgx,imgy):
      # Mandelbrot fractal
      # FB - 201003151
      from PIL import Image
      # drawing area (xa < xb and ya < yb)
      xa = -2.0
      xb = 1.0
      ya = -1.5
      yb = 1.5
      maxIt = 512 # iterations 256
      image = Image.new("RGB", (imgx, imgy))

      for y in range(imgy):
        cy = y * (yb - ya) / (imgy - 1)  + ya
        for x in range(imgx):
          cx = x * (xb - xa) / (imgx - 1) + xa
          c = complex(cx, cy)
          z = 0
          for i in range(maxIt):
              if abs(z) > 2.0: break
              z = z * z + c
          r = i % 4 * 64
          g = i % 8 * 32
          b = i % 16 * 16
          image.putpixel((x, y), b * 65536 + g * 256 + r)

      return image


    def generate_mandelbrot_fractal(self,imgx,imgy):
      # https://code.activestate.com/recipes/577111-mandelbrot-fractal-using-pil/
      # effect_mandelbrot
      # Mandelbrot fractal
      # FB - 201003254
      # drawing area
      xa = -2.0
      xb = 1.0
      ya = -1.5
      yb = 1.5
      maxIt = 255 # max iterations allowed
      image = Image.new("RGB", (imgx, imgy))

      for y in range(imgy):
        zy = y * (yb - ya) / (imgy - 1)  + ya
        for x in range(imgx):
          zx = x * (xb - xa) / (imgx - 1)  + xa
          z = zx + zy * 1j
          c = z
          for i in range(maxIt):
              if abs(z) > 2.0: break
              z = z * z + c
          image.putpixel((x, y), (i % 4 * 64, i % 8 * 32, i % 16 * 16))
      #image.save("mandel.png", "PNG")
      return image


    @trace(3)
    def on_draw_image_info(self,event):
      self.draw_image_info()


    @trace(3)
    def draw_image_info(self,image=None,show=True,color=None,filename=''):
      if image is None:
        image = self.rawimg
      if color is None:
        # TODO: need to covert to 'L' mode to get colors, why?
        # https://www.geeksforgeeks.org/python-pil-getcolors-method/
        im1 = image.convert("L")
        im2 = Image.Image.getcolors(im1)
        print(im2)
        color = 'black'
      if image is not None:
        if len(filename) <= 0:
          filename = self.filenamepath
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('arial.ttf', 18)
        draw.rectangle([(10, 10), (588, 32)], fill=(255,255,255), outline=(0,0,0))
        draw.text((23, 10), filename, fill='black', font=font)
        draw.rectangle([(image.width / 2 - len(color) * 10, 217), (image.width / 2 + len(color) * 10, 239)], fill=(255,255,255), outline=(0,0,0))
        draw.text((image.width / 2 - len(color) * 4, 218), color, fill='black', font=font)
        if show is True: self.display(image=image)


    @trace(3)
    def on_toggle_desktop_mode(self,event):
      self.toggle_desktop_mode()


    @trace(3)
    # TODO: image mode cycles through images in memory?
    def toggle_desktop_mode(self,toggle=True,value=True):
      """ Toggle image mode """
      if toggle is False:
        self.desktop_mode = value
      else:
        self.desktop_mode = not self.desktop_mode
      # TODO: apparently this isn't overwritten so theoretically i don't need to save just restove from the windows location
      if self.desktop_mode is True:
        loginfo("Desktop Mode ON")
        #C:\Users\Peter\AppData\Roaming\Microsoft\Windows\Themes\TranscodedWallpaper.jpg
        # https://stackabuse.com/how-to-copy-a-file-in-python/
        self.save_desktop_wallpaper()
        self.set_picture_position(self.picturepos)
      else:
        loginfo("Desktop Mode OFF")
        self.restore_desktop_wallpaper()
      self.display()


    @trace(3)
    def set_picture_position(self,pos):
      # set the wallpaper style
      # TODO: all wallpaper style to be changed and updated
      # https://stackoverflow.com/questions/14186400/setting-wallpaper-with-win-api
      # https://docs.python.org/3/library/winreg.html
      # HKEY_CURRENT_USER\Control Panel\Desktop "WallpaperStyle" and "TileWallpaper"
      # Fill = 10, Fit = 6, Stretch = 2, Tile = 1 ("TileWallpaper" = 1), Center = 0
      try:
        key = winreg.OpenKey( winreg.HKEY_CURRENT_USER, r'Control Panel\Desktop', 0,  access=winreg.KEY_READ)
        style,stype = winreg.QueryValueEx(key, "WallpaperStyle")
        tile,ttype = winreg.QueryValueEx(key, "TileWallpaper")
        loginfo("WallpaperStyle is",style,"TileWallpaper is",tile)
        key.Close()
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Control Panel\Desktop', 0,  access=winreg.KEY_WRITE)
        if int(style) != int(pos):
          loginfo("Setting WallpaperStyle to",pos)
          winreg.SetValueEx(key,"WallpaperStyle",0,winreg.REG_SZ,str(pos))
        if int(pos) == 1:
          if int(tile) != 1:
            loginfo("Setting TileWallpaper to",1)
            winreg.SetValueEx(key,"TileWallpaper",0,winreg.REG_SZ,str(1))
        else:
          if int(tile) == 1:
            loginfo("Setting TileWallpaper to",0)
            winreg.SetValueEx(key,"TileWallpaper",0,winreg.REG_SZ,str(0))
      except EnvironmentError as e:
        loginfo("Environment Error:",e)
      except Exception as e:
        exception(e)
      finally:
        key.Close()


    @trace(3)
    def on_toggle_image_mode(self,event):
      self.toggle_image_mode()


    @trace(3)
    # TODO: image mode cycles through images in memory?
    def toggle_image_mode(self,toggle=True,value=True):
      """ Toggle image mode """
      if toggle is False:
        self.image_mode = value
      else:
        self.image_mode = not self.image_mode
      if self.image_mode is True:
        loginfo("Image Mode ON")
        if len(self.images) > 0:
          self.rawimg = self.images[self.iimages].copy()
        else:
          self.close_images()
        self.display()
      else:
        loginfo("Image Mode OFF")
        if len(self.sources) > 0:
          self.open_file(ntpath.join(self.root_directory,self.sources[self.isources]))


    @trace(3)
    def on_toggle_frames_tool(self,event):
      self.toggle_frames_tool()


    # GIF's https://stackoverflow.com/questions/51523994/extract-key-frames-from-gif-using-python/51535698#51535698
    @trace(3)
    def toggle_frames_tool(self,toggle=True,value=True):
      """ Toggle debug mode """
      if toggle is False:
        loginfo("Not toggling, setting value to",value)
        self.show_tb_frametool = value
      else:
        self.show_tb_frametool = not self.show_tb_frametool
      loginfo("show_tb_frametool is",self.show_tb_frametool,", self.tb_frametool is",self.tb_frametool)
      if self.show_tb_frametool is True and self.tb_frametool not in self.tb_widgets:
        loginfo("Show Frame Tool")
        if self.tb_cmdtool in self.tb_widgets:
          loginfo("Hiding Command Tool")
          self.tb_cmdtool.pack_forget()
          self.tb_widgets.remove(self.tb_cmdtool)
        if self.tb_diagtool in self.tb_widgets:
          loginfo("Hiding Diag Tool")
          self.tb_diagtool.pack_forget()
          self.tb_widgets.remove(self.tb_diagtool)
        # show GIF frames tool
        frame_hud = '0'
        # TODO: frame tool label is not initialized on new image correctly
        if self.is_GIF_file is True: # so I can toggle when it's not a GIF to test, n_frames doesn't exist if it's not a GIF
          #frame_hud = str(self.rawimg.tell()) + "/" +  str(self.rawimg.n_frames)
          frame_hud = str(0) + "/" + str(self.rawimg.n_frames)
        self.initialize_frame_tool(self.toolbar,text=frame_hud,pack_only=True)

        #if self.show_tb_diagtool is True and self.tb_diagtool not in self.tb_widgets:
        #  self.initialize_diagnostics_tool(self.toolbar,pack_only=True)
        if self.show_tb_cmdtool is True and self.tb_cmdtool not in self.tb_widgets:
          self.initialize_command_tool(self.toolbar,pack_only=True)
      else:
        if self.tb_frametool in self.tb_widgets:
          loginfo("Hide Frame Tool")
          self.tb_frametool.pack_forget()
          self.tb_widgets.remove(self.tb_frametool)


    @trace(3)
    def on_toggle_debug(self,event):
      self.toggle_debug()


    @trace(3)
    def toggle_debug(self,toggle=True,value=True):
      """ Toggle debug mode """
      if toggle is False:
        self.debug = value
      else:
        self.debug = not self.debug
      loginfo("Debug Mode is",self.debug)
      self.toggle_diagnostics_tool(toggle=False,value=self.debug)


    @trace(3)
    def on_toggle_diagnostics_tool(self,event):
      self.toggle_diagnostics_tool()


    @trace(3)
    def toggle_diagnostics_tool(self,toggle=True,value=True):
      if toggle is False:
        self.show_tb_diagtool = value
      else:
        self.show_tb_diagtool = not self.show_tb_diagtool
      logverb("show_tb_diagtool is",self.show_tb_diagtool,",self.tb_diagtool is",self.tb_diagtool)
      if self.show_tb_diagtool is True:
        if self.tb_diagtool not in self.tb_widgets:
          loginfo("Showing Diagnostic Tool")
          if self.tb_cmdtool in self.tb_widgets:
            loginfo("Hiding Command Tool")
            self.tb_cmdtool.pack_forget()
            self.tb_widgets.remove(self.tb_cmdtool)

          # show diagnostic tool
          #self.initialize_diagnostics_tool(self.toolbar,pack_only=True)

          if self.show_tb_cmdtool is True and self.tb_cmdtool not in self.tb_widgets:
            self.initialize_command_tool(self.toolbar,pack_only=True)
      else:
        if self.tb_diagtool in self.tb_widgets:
          loginfo("Hide Diagnostic Tool")
          self.tb_diagtool.pack_forget()
          self.tb_widgets.remove(self.tb_diagtool)


    @trace(3)
    def on_toggle_command_tool(self,event):
      self.toggle_command_tool()


    @trace(3)
    def toggle_command_tool(self,toggle=True,value=True):
      if toggle is False:
        self.show_tb_cmdtool = value
      else:
        self.show_tb_cmdtool = not self.show_tb_cmdtool
      loginfo("show_tb_cmdtool is",self.show_tb_cmdtool,"self.tb_cmdtool is",self.tb_cmdtool)
      if self.show_tb_cmdtool is True:
        if self.tb_cmdtool not in self.tb_widgets:
          if self.widgets_on is True:
            loginfo("Show Command Tool")
            # show command tool
            self.initialize_command_tool(self.toolbar,setfocus=True,pack_only=True)
          else:
            self.show_tb_cmdtool = False # set to false to avoid double toggle to toggle
      else:
        if self.tb_cmdtool is not None:
          if self.tb_cmdtool in self.tb_widgets:
            loginfo("Hide Command Tool")
            self.tb_cmdtool.pack_forget()
            self.tb_widgets.remove(self.tb_cmdtool)
            if self.picture_frame is not None: self.picture_frame.focus_set()


    @trace(3)
    def display_width(self):
      return self.master.winfo_width() - 4


    @trace(3)
    def display_height(self):
      if self.fullscreen_mode is True or self.widgets_on is False:
        return self.master.winfo_height()
      else:
        # using self.statusbar_thickness set when statusbar is created because the status bar height returned will
        # fluctuate and as such I need to enforce the height not obtain it. This would not be an issue if the statusbar
        # was properly anchored to bottom of the window but the only anchor I could find has to do with text alignment.
        # The picture frame size will push down the statusbar as the window pushes up squeezing it
        # The toolbar is fine for now as it is at the top and isn't being squeezed by the shrinking window
        #logverb("Toolbar height:",self.toolbar.winfo_height(),"Statusbar height",self.statusbar.winfo_height())
        return self.master.winfo_height() - self.toolbar.winfo_height() - self.statusbar_thickness - 4


    def verify_aspect_ratio(self,image,size,tolerance=0.002,log=False):
      """ Checks the aspect ratio of an image vs the size to see if the size maintains the apsect ratio within the specified tolerance with a default of 0.002. """
      r1 = size[0] / image.width
      r2 = size[1] / image.height
      r1r = round(r1,3)
      r2r = round(r2,3)
      loginfo("Width ratio:",r1r,", Height ratio:",r2r,";  Abs:", r1,"and",r2)
      if math.isclose(r1r,r2r,abs_tol=tolerance) is not True:
        msg = "Width vs Height Ratio is not accurate to 3 places!\nWidth ratio is: "+str(r1r)+", Height ratio is: " +str(r2r)+"\nTotal Width ratio is: "+str(r1)+", Total Height ratio is: " +str(r2)+"\n"+"Width:: New Size: "+str(size[0])+" / Original Size: "+str(image.width)+"\nHeight:: New Size: "+str(size[1])+" / Original Size: "+str(image.height)
        logwarn("Image Distortion",msg)
        if self.show_ui_error_messages is True:
          messagebox.showerror("Image Distortion",msg)
        if log is True:
          if self.image_mode is False:
            self.log("Resize Accuracy Data\n"+ntpath.join(self.root_directory,self.sources[self.isources])+"\n"+msg)
          else:
            self.log(self.image_name,"\n",msg)
        return False
      return True


    @trace(3)
    def get_resized_img(self,image,size):
      """ Resize to specified dimensions exactly, does not maintain aspect ratio. """
      # DONE: hit OSError in ImageFile.py line 255 in this next call when resizing window at same time so wrap in a try catch
      # https://www.geeksforgeeks.org/python-pil-image-resize-method/
      # https://pillow.readthedocs.io/en/stable/reference/Image.html
      # TODO: used thumnail by default but add switch to do comparisons
      # check height width ratio
      self.verify_aspect_ratio(image,size)
      loginfo("New Size is ", size)
      try:
        # make sure LOAD_TRUNCATED_IMAGES is off so we can see files with errors
        ImageFile.LOAD_TRUNCATED_IMAGES = False # also works on broken data streams apparently
        resized_image = image.resize(size) # was resample=Image.ANTIALIAS, default is resample=3
      except OSError as e:
        logwarn(e)
        if self.show_ui_error_messages is True:
          messagebox.showerror("File Error",e)
        self.stauserrorlbl.config(text="File Error: "+ str(e))
        if self.image_mode is False:
          #print(self.isources,len(self.sources))
          #print(self.sources)
          #print(self.root_directory)
          self.log("File Error\n"+str(e)+"\n"+ntpath.join(self.root_directory,self.sources[self.isources]))
        else:
          self.log("File Error\n"+str(e)+"\n"+self.image_name)
        ImageFile.LOAD_TRUNCATED_IMAGES = True # this is truncated or broken to try again with flag set
        resized_image = image.resize(size)
        # if not having his flag set causes issues anywhere else I want to know so i'm keeping it off
      finally:
        ImageFile.LOAD_TRUNCATED_IMAGES = self.load_trunc
      return resized_image


    @trace(3)
    def get_resized_img_fit(self,image,size=None):
      # TODO: pri=3;sev=0; resize images to set size using pixels or other methods so I can output exact size images
      #self.resize = True # deprecated; doesn't make sense to set this here, flag is to prompt a resize
      #print("Status Bar Width",self.statusbar.winfo_width())
      #print("Master Width",self.master.winfo_width())
      #if self.fullscreen is True:
      #height = self.master.winfo_height() - self.statusbar.winfo_height() - self.toolbar.winfo_height() - 16
      #else:
      if size is None:
        width,height = self.display_width(),self.display_height()
        loginfo("Display Size: Width",width,", Height",height)
      else:
        width,height = size
        loginfo("Custom Size: Width",width,", Height",height)
        height,width = size
      #image.thumbnail((height,width))
      #return image
      # deprecated
      display_ratio = width / height
      image_ratio = image.size[0] / image.size[1]
      loginfo("Display Ratio", display_ratio,"To Image Ratio",image_ratio)
      if display_ratio >= 1:  # the display is wide (or square i believe)
        if image_ratio <= display_ratio:  # image is not wide enough
          width_new = int(height * image_ratio)
          size_new = width_new, height
        else:  # image is wider than display
          height_new = int(width / image_ratio)
          size_new = width, height_new
      else:  # the video is tall
        if image_ratio >= display_ratio:  # image is not tall enough
          height_new = int(width / image_ratio)
          size_new = width, height_new
        else:  # image is taller than display
          width_new = int(height * image_ratio)
          size_new = width_new, height
      if self.verify is True:
        self.verify_aspect_ratio(image,size_new,log=self.verify)
      #return image
      return self.get_resized_img(image,size_new)


    @trace(3)
    def get_resized_img_fill(self,image,size=None):
      # TODO: pri=3;sev=0; resize images to set size using pixels or other methods so I can output exact size images
      #self.resize = True # deprecated; doesn't make sense to set this here, flag is to prompt a resize
      #print("Status Bar Width",self.statusbar.winfo_width())
      #print("Master Width",self.master.winfo_width())
      #if self.fullscreen is True:
      #height = self.master.winfo_height() - self.statusbar.winfo_height() - self.toolbar.winfo_height() - 16
      #else:
      if size is None:
        width,height = self.display_width(),self.display_height()
        loginfo("Display Size: Width",width,", Height",height)
      else:
        loginfo("Custom Size: Width",width,", Height",height)
        width,height = size
      image.thumbnail((max(height,width),max(height,width)))
      display_ratio = width / height
      image_ratio = image.size[0] / image.size[1]
      loginfo("Display Ratio", display_ratio,"To Image Ratio",image_ratio)
      if display_ratio >= 1:  # the display is wide
        if image_ratio <= display_ratio:  # image is not wide enough
          width_new = int(height * image_ratio)
          size_new = width_new, height
        else:  # image is wider than display
          height_new = int(width / image_ratio)
          size_new = width, height_new
      else:  # the display is tall
        if image_ratio >= display_ratio:  # image is not tall enough
          height_new = int(width / image_ratio)
          size_new = width, height_new
        else:  # image is taller than display
          width_new = int(height * image_ratio)
          size_new = width_new, height
      # DONE: hit OSError in ImageFile.py line 255 in this next call when resizing window at same time so wrap in a try catch
      # https://www.geeksforgeeks.org/python-pil-image-resize-method/
      # https://pillow.readthedocs.io/en/stable/reference/Image.html
      if self.verify is True:
        self.verify_aspect_ratio(image,size_new,log=self.verify)
      return image
      return self.get_resized_img(image,size_new)


    @trace(3)
    def on_foo(self,event):
      self.foo()


    @trace(3)
    def foo(self):
      loginfo("What you talkin bout foo?")


    @trace(3)
    def on_bar(self,event):
      self.bar()


    @trace(3)
    def bar(self):
      loginfo("YOU SHALL NOT PASS DEMON OF THE .... ehem, hold on, excuse me, I didn't have my glasses on I'm very sorry about that you may pass")


    @trace(3)
    def on_slate(self,event):
      self.slate()


    @trace(3)
    def slate(self):
      loginfo("Changing Background to Slate")
      self.set_window_color('#333333')


    @trace(3)
    def on_white(self,event):
      self.white()


    @trace(3)
    def white(self):
      loginfo("Changing Background to White")
      self.set_window_color('#FFFFFF')


    @trace(3)
    def on_black(self,event):
      self.black()


    @trace(3)
    def black(self):
      loginfo("Changing Background to Black")
      self.set_window_color('#000000')


    def on_zoom_in(self,event):
      self.zoom_in()


    @trace(3)
    def zoom_in(self):
      loginfo("Zoom IN")
      self.zoomed = True
      self.resize = False
      self.zoom = self.zoom + self.zoom_incdec
      self.display()


    @trace(3)
    def on_zoom_out(self,event):
      self.zoom_out()


    @trace(3)
    def zoom_out(self):
      loginfo("Zoom OUT")
      self.zoomed = True
      self.resize = False
      self.zoom = self.zoom - self.zoom_incdec
      self.display()


    @trace(3)
    # https://www.geeksforgeeks.org/transparent-window-in-tkinter/
    def on_increase_alpha(self,event):
     self.increase_alpha()


    @trace(3)
    def increase_alpha(self):
      if self.alpha <= 0.9:
        self.alpha = round(math.fsum([self.alpha,0.1]),1)
        loginfo("Setting Alpha to",self.alpha)
        self.master.attributes('-alpha',self.alpha)
      elif self.alpha < 1.0:
        self.alpha = 1.0
        loginfo("Setting Alpha to",self.alpha)
        self.master.attributes('-alpha',self.alpha)


    @trace(3)
    def on_decrease_alpha(self,event):
     self.decrease_alpha()


    @trace(3)
    def decrease_alpha(self):
      if self.alpha >= 0.1:
        self.alpha = round(math.fsum([self.alpha,-0.1]),1)
        loginfo("Setting Alpha to",self.alpha)
        self.master.attributes('-alpha',self.alpha)
      elif self.alpha > 0.0:
        self.alpha = 0.0
        loginfo("Setting Alpha to",self.alpha)
        self.master.attributes('-alpha',self.alpha)


    @trace(3)
    def on_transparent(self,event):
      self.transparent()


    @trace(3)
    def transparent(self):
      self.toggle_transparency(toggle=False,value=True)


    @trace(3)
    def on_toggle_transparency(self,event):
        self.toggle_transparency()


    @trace(3)
    def toggle_transparency(self,toggle=True,value=True):
      if toggle is False:
        self.transparency = value
      else:
        self.transparency = not self.transparency
      if self.transparency is True:
        loginfo("Transparency is ON")
        # set color to Transparency Mask
        self.set_window_color('#123456') # secret code ;)-
      else:
        loginfo("Transparency is OFF")
        self.set_window_color(self.color)


    def on_help(self,event):
      self.usage()


    def usage(self):
      loginfo("You must be a wizard to use this magic device!")


    @trace(3)
    def on_tool(self,event):
        self.tool()


    @trace(3)
    def tool(self):
      self.set_window_style('tool')


    @trace(3)
    def on_widget(self,event):
      self.widget()


    @trace(3)
    def widget(self):
      self.set_window_style('widget')


    @trace(3)
    def on_compact(self,event):
        self.compact()


    @trace(3)
    def compact(self):
      self.set_window_style('compact')


    @trace(3)
    def on_normal(self,event):
        self.normal()


    @trace(3)
    def normal(self):
      self.set_window_style('normal')


    @trace(3)
    def on_widescreen(self,event):
        self.widescreen()


    @trace(3)
    def widescreen(self):
      self.set_window_style('widescreen')


    @trace(3)
    def on_toggle_zoom(self,event):
        self.toggle_zoom()


    @trace(3)
    def toggle_zoom(self,toggle=True,value=True):
      # TODO: not resizing properly sometimes when toggling zoom but I have no repro currently, believe I toggled F2 then F3 but there is more to it that I can't seem to replicate now I added and commented out display to try to fix then repro.
      if toggle is False:
        self.zoom_on = value
      else:
        self.zoom_on = not self.zoom_on
      if self.zoom_on is True:
        loginfo("Zoom is ON")
        self.geometry = self.master.geometry()
        loginfo("Geometry",self.geometry)
        # https://stackoverflow.com/questions/15981000/tkinter-python-maximize-window
        #self.master.attributes('-zoomed', True) # NA on Window?
        self.master.state('zoomed')
        self.zoom_widgets_on = self.widgets_on
        self.hide_widgets()
        #self.master.overrideredirect(True) # removes the title bar according to comments
      else:
        loginfo("Zoom is OFF")
        # https://stackoverflow.com/questions/15981000/tkinter-python-maximize-window
        #self.master.overrideredirect(False)
        #self.master.attributes('-zoomed', False) # NA on Window?
        self.master.state('normal')
        if self.zoom_widgets_on is True:
          self.show_widgets()
        loginfo("Geometry",self.geometry)
        #self.master.geometry(self.geometry)
      #self.display()


    # https://www.delftstack.com/howto/python-tkinter/how-to-create-full-screen-window-in-tkinter/
    # https://www.geeksforgeeks.org/how-to-create-full-screen-window-in-tkinter/
    @trace(3)
    def on_fullscreen(self,event):
      self.fullscreen()


    @trace(3)
    def fullscreen(self):
      self.master.attributes('-fullscreen', True)
      self.fullscreen_mode = True
      #self.master.wm_attributes('-fullscreen', 1)
      loginfo("Fullscreen Mode")
      self.master.attributes('-fullscreen', True)
      self.hide_widgets()


    @trace(3)
    def on_windowed(self,event):
      self.windowed()


    @trace(3)
    def windowed(self):
      self.master.attributes('-fullscreen', False)
      self.fullscreen_mode = False
      loginfo("Windowed Mode")
      self.master.attributes('-fullscreen', False)
      self.master.attributes('-alpha',1.0)
      if self.widgets_on is True:
        self.show_widgets()
      key_press = time.time_ns() / (10 ** 9)
      if key_press < self.last_esc_key_press + self.time_window:
        loginfo("Double Tap Detected! Resetting Window.")
        self.master.state('normal') # zoom state, will block setting geometry if in 'zoom' mode
        self.set_window_style('normal') # resize window
      loginfo("Last Keypress",self.last_esc_key_press,"Window",key_press + self.time_window)
      self.last_esc_key_press = key_press


    @trace(3)
    def on_restore(self,event):
      self.restore()


    @trace(3)
    def restore(self,og=True):
      if og is True:
        self.set_window_style('normal') #
      self.master.attributes('-fullscreen', False)


    @trace(3)
    def on_toggle_fullscreen(self,event):
      self.toggle_fullscreen()


    @trace(3)
    # DONE: reset window size to original for extra safety, windows can get too big to handle easily sometimes
    # TODO: add taskbar option using w.iconify() or root.wm_state('iconic') # https://stackoverflow.com/questions/4481880/minimizing-a-tk-window
    # https://stackoverflow.com/questions/22834150/difference-between-iconify-and-withdraw-in-python-tkinter
    # https://stackoverflow.com/questions/46387629/iconify-in-tkinter-in-python
    def toggle_fullscreen(self,toggle=True,value=True):
       #self.master.state('zoomed')
      if toggle is False:
        self.fullscreen_mode = value
      else:
        self.fullscreen_mode = not self.fullscreen_mode
      #if self.master.cget('fullscreen') is True:
      if self.fullscreen_mode is True:
        self.fullscreen()
      else:
        self.windowed()


    @trace(3)
    def on_prev_cmd_history(self,event):
      self.prev_cmd_history()


    @trace(3)
    def prev_cmd_history(self):
      loginfo("Command History length is", len(self.command_history))
      if len(self.command_history) > 0:
        if self.icommand_history > 0:
          self.icommand_history = self.icommand_history - 1
        loginfo("Previous Command:: Index:",self.icommand_history,"Cmd:",self.command_history[self.icommand_history])
        self.cmd.set(self.command_history[self.icommand_history])
        self.command_line.icursor(END) # TODO: I tried (-1) but that didn't work, 1000 is a hack, find appropriate fix


    @trace(3)
    def on_next_cmd_history(self,event):
      self.next_cmd_history()


    @trace(3)
    def next_cmd_history(self):
      # TODO: prev ends up needing two next clicks to get to next from first if prev was clicked on the first one at least twice
      # TODO: after entering last command next shows last command, should this just be past the end of the history at the blank new entry? I think its currently the history index is before the last not after.
      loginfo("Command History length is", len(self.command_history))
      if len(self.command_history) > 0:
        if self.icommand_history < len(self.command_history):
          self.icommand_history = self.icommand_history + 1
        if self.icommand_history < len(self.command_history):
          loginfo("Next Command:: Index:",self.icommand_history,"Cmd:",self.command_history[self.icommand_history])
          self.cmd.set(self.command_history[self.icommand_history])
          self.command_line.icursor(END) # hack for now to get the caret to the end of the line (i think, adding comments @ late date and a glance)
        else:
          loginfo("Clearing command bar for new command")
          self.cmd.set('')
      #else:
      #  self.cmd.set('')


    @trace(3)
    def on_process_command(self,event):
      self.process_command()


    @trace(3)
    def process_command(self):
      """ Process commands entered into the command bar """
      commands = {
        'toggle filters': self.toggle_filters,
        'toggle blur': self.toggle_blur,
        'toggle contour': self.toggle_contour,
        'toggle enhance': self.toggle_enhance,
        'toggle enhance more': self.toggle_enhance_more,
        'toggle emboss': self.toggle_emboss,
        'toggle edges': self.toggle_edges,
        'toggle sharpen': self.toggle_sharpen,
        'toggle smooth': self.toggle_smooth,
        'toggle smooth more': self.toggle_smooth_more,
        'toggle detail': self.toggle_detail,
        'add filters': self.toggle_filters,
        'add blur': self.toggle_blur,
        'add contour': self.toggle_contour,
        'add enhance': self.toggle_enhance,
        'add enhance more': self.toggle_enhance_more,
        'add emboss': self.toggle_emboss,
        'add edges': self.toggle_edges,
        'add sharpen': self.toggle_sharpen,
        'add smooth': self.toggle_smooth,
        'add smooth more': self.toggle_smooth_more,
        'add detail': self.toggle_detail,
        'clear filters': self.clear_selected_filters,
        'remove blur': self.toggle_blur,
        'remove contour': self.toggle_contour,
        'remove enhance': self.toggle_enhance,
        'remove enhance more': self.toggle_enhance_more,
        'remove emboss': self.toggle_emboss,
        'remove edges': self.toggle_edges,
        'remove sharpen': self.toggle_sharpen,
        'remove smooth': self.toggle_smooth,
        'remove smooth more': self.toggle_smooth_more,
        'remove detail': self.toggle_detail,
        'resize image' : self.img_resize,
        'origional image' : self.img_origional,
        'random image' : self.file_random,
        'bg' : None, # set background color, one arg - color
        'test' : self.perform_self_test,
        '---' : self.insert_seperator,
        'debug' : self.toggle_debug,
        'verb' : self.cycle_trace_verbosity,
        'trace' : self.cycle_bb_verbosity,
        'start' : self.start,
        'stop' : self.stop,
        'home' : self.go_to_first_slide,
        'end' : self.go_to_last_slide,
        'up' : self.go_to_prev_directory,
        'down' : self.go_to_next_directory,
        'interval': self.set_interval,
        'new filter' : self.new_filter,
        'new aggregate' : self.new_aggregate_filter,
        'v' : self.toggle_privacy,
        'private' : self.toggle_privacy,
        'hide' : self.toggle_privacy,
        'a' : self.new_aggregate_filter,
        'b' : self.toggle_blur,
        'c' : self.toggle_contour,
        'e' : self.toggle_emboss,
        'd' : self.toggle_detail,
        'g' : self.toggle_edges,
        'h' : self.toggle_enhance,
        'i' : self.toggle_filters,
        'l' : self.toggle_repeat,
        'm' : self.toggle_smooth,
        'n' : self.new_filter,
        'o' : self.img_origional,
        'p' : self.toggle_sharpen,
        'r' : self.file_random,
        's' : self.toggle_resize,
        'w' : self.img_resize,
        'x' : self.clear_selected_filters,
        'y' : self.toggle_grayscale,
        'z' : self.toggle_random,
        #'z' : self.toggle_menu,
        'prev' : self.file_prev,
        'next' : self.file_next,
        'edit filter mode' : None,
        'filter' : None,
        'dump' : None,
        'exit' : self.toggle_command_tool,
        'cls' : self.clearscreen,
        'geometry' : None,
        'make' : None,
        'picturepos': None,
        # TODO: pri=0;sev=0; 'file $pathfilename' : open_image_file
        # TODO: pri=0;sev=0; 'save $pathfilename : save_image_to_file
        # TODO: pri=0;sev=0; 'load $command_script.csi : load_commands_from_file
      }
      processed = False
      # https://effbot.org/tkinterbook/variable.htm
      #print(self.cmd.get())
      #print("That's a little bit harsh don't you think?")
      command_text = self.cmd.get().strip()
      loginfo("Command Text is '"+command_text+"'")
      cmdline = command_text.split(' ', 2)
      loginfo("cmdline",cmdline)
      loginfo("Split Command Line is", cmdline)
      command = cmdline[0].strip().lower()
      if command_text in self.command_history:
        self.command_history.remove(command_text) # remove so no duplicates and since appended again it will be re-ordered to the top of the pile
      if len(cmdline) > 1:
        cmdnmod = cmdline[0].strip() + " " + cmdline[1].strip()
      else:
        cmdnmod = command
      loginfo("Command is '" + command + "'")
      if command == 'toggle':
        call = commands.get(cmdnmod,None)
        if call is not None:
          call()
          processed = True
      elif command == 'add':
        call = commands.get(cmdnmod,None)
        if call is not None:
          call(toggle=False,value=True)
          processed = True
      elif command == 'remove':
        call = commands.get(cmdnmod,None)(toggle=False,value=False)
        if call is not None:
          call(toggle=False,value=False)
          processed = True
      elif command == 'new':
        if len(cmdline) > 1 and cmdline[1] == 'filter':
          call = commands.get(cmdnmod,None)
          if call is not None:
            call()
            processed = True
        elif len(cmdline) > 2 and cmdline[1] == 'filter':
          call = commands.get(cmdnmod,None)
          if call is not None:
            call(cmdline[2])
            processed = True
        else:
          call = commands.get(cmdnmod,None)
          if call is not None:
            call()
            processed = True
      elif command == 'interval':
        if len(cmdline) > 1:
          loginfo("New Interval is",cmdline[1])
          call = commands.get(command,None)
          if call is not None:
            call(float(cmdline[1]))
            processed = True
      elif command == 'private' or command == 'hide':
        call = commands.get(cmdnmod)
        if call is not None:
          call(toggle=False,value=True)
          processed = True
      elif cmdline == "edit filter mode" or cmdline == "edit filter mode on":
        self.edit_filter_mode = True
        processed = True
      elif cmdline == "edit filter mode off":
        self.edit_filter_mode = False
        processed = True
      elif command == 'bg':
        if len(cmdline) > 1:
          color=bg=cmdline[1].strip().lower()
          self.set_window_color(color)
          self.color = color
          processed = True
      elif command == 'filter':
        if command in commands and len(cmdline) > 1 and cmdline[1].strip().lower() in self.custom_filters: # i can take it out if I want to disable without removing this code
          self.selected_filters.clear()
          # start at one and loop around because 0 is not physically before one on top of the keyboard
          self.ishortcuts = (self.ishortcuts + 1) % 10 # there are 10 number keys. won't change, wont' be used elsewhere
          loginfo("Custom Filter",self.ishortcuts,"is",cmdline[1].strip().lower())
          for f in self.custom_filters[cmdline[1].strip().lower()]:
            self.selected_filters.append(f)
          self.shortcuts[self.ishortcuts] = [] # make sure it knows its a list
          for f in self.custom_filters[cmdline[1].strip().lower()]:
            self.shortcuts[self.ishortcuts].append(f)
          loginfo("Shortcuts:",self.shortcuts)
          if self.ishortcuts not in self.keybindings: # or self.keybindings[self.ishortcuts] is None
            #self.picture_frame.unbind(self.keybindings[self.ishortcuts])
            self.keybindings[self.ishortcuts] = self.picture_frame.bind(str(self.ishortcuts), self.on_shortcut)
          processed = True
          loginfo("Selected Filters:: Shortcut Key:",self.ishortcuts,", Filters:",self.selected_filters)
          self.filterimg = True
          self.display()
        else:
          logwarn("Filter Command '"+command_text+"' Not Recognized!")
      elif command == 'dump':
        if len(cmdline) > 1:
          if command in commands:
            if cmdline[1].strip().lower() == 'sources':
              if len(self.sources):
                  print("\nDumping Sources -")
                  print("First File:",ntpath.join(self.root_directory,self.sources[0]))
                  print("Last File:",ntpath.join(self.root_directory,self.sources[-1]))
                  print(len(self.sources),"Image Sources Found")
                  print("Source Index is", self.isources)
                  print("----------- BEGIN SOURCE DUMP ---------------")
                  for source in self.sources:
                    if len(cmdline) > 2:
                      if cmdline[2].strip().lower() not in (ntpath.join(self.root_directory,source)).lower():
                        continue
                    print(ntpath.join(self.root_directory,source))
                  print("----------- END SOURCE DUMP -----------------")
              else:
                print("No Sources Found!")
              processed = True
          else:
            logwarn("No such",command,"command",cmdline[1].strip().lower())
        else:
          loginfo("Please specify what to dump, [ sources, ]")
      elif command == 'pil':
        if len(cmdline) > 1 and cmdline[1].strip().lower() == 'help':
          help(ImageFilter.BLUR)
          processed = True
      elif command == 'geometry':
        if len(cmdline) > 1 and cmdline[1].strip() in self.windows_geometries:
          loginfo("Setting Geometry to",cmdline[1].strip())
          self.set_window_style(cmdline[1].strip())
          processed = True
      elif command == 'make':
        if len(cmdline) > 1 and cmdline[1].strip().lower() == 'icons':
          self.make_icons_from_image()
          processed = True
      elif command == 'picturepos':
        if len(cmdline) > 1:
          value = int(cmdline[1].strip())
          if value >= 0 and value <= 10:
            self.set_picture_position(value)
            self.picturepos = value
            processed = True
            self.display()
      else:
        loginfo('Command Length =',len(command))
        if len(command) == 1 and command.isdigit() and int(command) >= 0 and int(command) <= 10:
          self.shortcut(int(command))
        call = commands.get(cmdnmod,None)
        if call is not None:
          call()
          processed = True
        else:
          logwarn("Commands Not Found and Text Entered '"+command_text+"' Not Recognized!")
          return
      self.cmd.set('')
      if processed is True:
        self.command_history.append(command_text)
        self.icommand_history = len(self.command_history)


    @trace(3)
    def on_shortcut(self,event):
      loginfo("Event", event)
      self.shortcut(int(event.char))


    @trace(3)
    def shortcut(self,key):
      assert key >= 0 and key <= 9, "Key " + key + "is not valid"
      loginfo("Length:: key:",key,", shortcuts:",len(self.shortcuts))
      loginfo("Shortcuts",self.shortcuts)
      if key in self.shortcuts:
        self.selected_filters.clear()
        for f in self.shortcuts[key]:
          self.selected_filters.append(f)
        loginfo(len(self.selected_filters),"Selected Filters:: Shortcut Key:",key,", Filters:",self.selected_filters)
        self.filterimg = True
        self.ishortcuts = key
        self.display()


    @trace(3)
    def disable(self):
      # DONE: enable disable picture buttons
      """ Set application to the disabled but ready to use state """
      logverb("Disabling Application")
      if self.toolbar is not None:
        #self.savebtn['state'] = DISABLED # after first being enabled there should always be a file present
        self.prevbtn['state'] = DISABLED
        self.nextbtn['state'] = DISABLED
        self.luckybtn['state'] = DISABLED
        self.showbtn['state'] = DISABLED
        self.repeatbtn['state'] = DISABLED
        self.shufflebtn['state'] = DISABLED
        self.randombtn['state'] = DISABLED
        self.leftbtn['state'] = DISABLED
        self.rightbtn['state'] = DISABLED
        #self.seekprevbtn['state'] = DISABLED
        #self.seeknextbtn['state'] = DISABLED


    @trace(3)
    def enable(self):
      """ Set application to enabled state """
      logverb("Enabling Application")
      if self.toolbar is not None:
        self.savebtn['state'] = NORMAL
        self.prevbtn['state'] = NORMAL
        self.nextbtn['state'] = NORMAL
        self.luckybtn['state'] = NORMAL
        self.showbtn['state'] = NORMAL
        self.repeatbtn['state'] = NORMAL
        self.shufflebtn['state'] = NORMAL
        self.randombtn['state'] = NORMAL
        self.leftbtn['state'] = NORMAL
        self.rightbtn['state'] = NORMAL
        #self.seekprevbtn['state'] = NORMAL
        #self.seeknextbtn['state'] = NORMAL


    @trace(3)
    def clearscreen(self):
      os.system('cls')


    @trace(3)
    def perform_self_test(self):
      """ Perform a self test ... I'll get to it! """
      print("This is a test, this is only a ... wait a minute! \nOMG, we're all gonna die, run for your lives! AAAAAAAAHHHHHHHHHH!\nNo wait, ummmmmm .... sorry, false alarm")
      print("Self Destruct in 5, 4, 3, 2, 1 ... what are you waiting for?")
      print("But Seriously Folks, Now Performing A Self Test")
      print("The Test Has PASSED! Hurray! Do you believe me? \nI know it was awful quick but as the kids say now-a-days 'there is nothing you can do about it'")


    @trace(3)
    def insert_seperator(self):
      """ Print trace seperator that is easy to see when scrolling with time date stamp for identification """
      date = datetime.now()
      loginfo("*************************************************")
      loginfo("----- ***",date," *** -------")
      loginfo("*************************************************")


    @trace(3)
    def cycle_trace_verbosity(self,cycle=True,level=0):
      """ Cycle through the trace levels """
      if cycle is True:
        level = gettracelevel()
        loginfo("Trace level is",level)
        level = (level + 1) % 7
        loginfo("New Trace level is",level)
        settracelevel(level)
        loginfo("Trace Level set is",gettracelevel())
        self.tracelevel.set(level)
      else:
        settracelevel(level)
        self.tracelevel.set(level)


    @trace(3)
    def cycle_bb_verbosity(self,cycle=True,level=0):
      """ Cycle through the trace levels """
      if cycle is True:
        level = getlevelasvalue()
        loginfo("BlackBox level is",level)
        level = (level + 1) % len(levels)
        loginfo("New BlackBox level is",level)
        setlevelasvalue(level)
        loginfo("BlackBox Level set is",getlevel())
        self.bblevel.set(getlevel())
      else:
        setlevelasvalue(level)
        self.bblevel.set(getlevel())


    @trace(3)
    def get_file_path_info(self,filepath):
      #self.root_directory = os.path.dirname(filepath)
      self.filenamepath = filepath
      self.file_name,self.file_ext = self.get_file_name_ext(filepath)
      if len(filepath) < 4:
        logerror("Invalid Path Name",filepath)
        self.stauserrorlbl.config(text="Error: Invalid Path Name ->" + filepath)
      return filepath


    @trace(3)
    def get_file_name_ext(self,filepath):
      logverb("Filepath:",filepath)
      filenameext = os.path.basename(filepath)
      root_ext_pair = os.path.splitext(filenameext)
      filename = root_ext_pair[0]
      ext = root_ext_pair[1].strip('.')
      if len(ext) <= 0: ext = None
      logverb("Filename:", filename, ", Extension:", ext)
      return filename,ext


    @trace(3)
    def process_command_line_arguments(self):
      """ Process any command line parameters """
      # DONE: FIX when selecting a drive like C:\ I get c:auvid_files\files.foo in my python image dir
      # TODO: do better command line parsing using ArgParse
      # TODO: use glob.glob and a command line option to get just a directory vs. a whole tree
      loginfo("Command line is", sys.argv)
      if len(self.targets) == 1: # file or directory
        arg = self.targets[0]
        self.filenamepath = os.path.abspath(arg)
        self.root_directory = os.path.dirname(self.filenamepath)
        #self.get_file_path_info(self.filenamepath)
        loginfo("Argument is",self.filenamepath)
        if os.path.isdir(self.filenamepath):
          loginfo("Searching ...",self.filenamepath)
          if self.process_input_dir(self.filenamepath) is True:
            self.open_files(self.filenamepath)
        elif os.path.isfile(self.filenamepath):
          loginfo("Loading...",self.filenamepath)
          if self.process_input_path(self.filenamepath) is True:
            self.sources = self.ordered_sources
            self.open_file(self.filenamepath,append=True)
        else: loginfo("Error: Argument provided was not a valid path or filename ->",arg)
      elif len(self.targets) > 1: # user specified more then one file or directory
        for arg in self.targets:
          if os.path.isdir(arg):
            pass
          elif os.path.isfile(arg):
            self.sources.append(arg)
          else: loginfo("Error: Argument provided was not a valid path or filename ->",arg)
        # TODO: need to seperate open_files so I can use the crawl functionality here
        if len(self.sources) > 0:
          loginfo("Sources",self.sources)
          self.isources = 0
          path = os.path.abspath(self.sources[self.isources])
          loginfo("Root Path is", path)
          self.root_directory = ''
          #self.root_directory = self.filenamepath[:len(self.sources[self.isources])]
          #loginfo("Root Directory is", self.root_directory)
          self.open_file(path)
          self.enable()


    @trace(3)
    def copy_image(self,image):
      ImageFile.LOAD_TRUNCATED_IMAGES = False
      try:
        image = image.copy()
      except OSError as e:
        self.stauserrorlbl.config(text="Error: " + str(e))
        logwarn(e)
        if self.show_ui_error_messages is True:
          messagebox.showerror("File Error",e)
        if self.image_mode is False:
          self.log("File Error\n"+str(e)+"\n"+self.filenamepath)
        else:
          self.log("File Error\n"+str(e)+"\n"+self.image_name)
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        image = image.copy()
      finally:
        ImageFile.LOAD_TRUNCATED_IMAGES = self.load_trunc
      return image


    @trace(3)
    def apply_filters(self,image):
      self.filtimg = self.copy_image(image)
      #self.filtimg = self.rawimg
      # It's quite common for algorithms to be unable to work with a palette based image
      # https://stackoverflow.com/questions/10323692/cannot-filter-palette-images-error-when-doing-a-imageenhance-sharpness
      if self.filtimg.palette is not None or self.filtimg.mode == 'P': # ValueError: cannot filter palette images
          assert self.filtimg.palette is not None and self.filtimg.mode == 'P',"Palette and Mode are Mismatched, Image is Corrupted!"
          loginfo("Converting Paletted Image to RGB")
          self.filtimg = self.filtimg.convert('RGB') # convert to full RGB at each pixel location
      if self.test is True and self.filterimg is True:
        loginfo("Converting Image to '1'")
        self.filtimg = self.filtimg.convert('1')
        # https://pythontic.com/image-processing/pillow/attributes
        #self.filtimg = image.convert("P", palette=Image.ADAPTIVE, colors=16)
      if len(self.selected_filters) and self.filterimg is True:
        loginfo("Applying",len(self.selected_filters),"Selected Filters",self.selected_filters,"...")
        for filter in self.selected_filters:
          if self.edit_filter_mode is True: print(repr(filter).strip(r"class <'>"))
          self.filtimg = self.filtimg.filter(filter) # apply filters
      if self.grayscale == True and self.filterimg is True:
        loginfo("Converting to Grayscale")
        self.filtimg = ImageOps.grayscale(self.filtimg)
      if self.privacy is True: # last to enforce privacy seperately
        loginfo("Privacy Mode Enforced")
        self.filtimg = self.filtimg.filter(ImageFilter.GaussianBlur(radius=100))
      return self.filtimg


    @trace(3)
    def apply_effects(self,image):
      self.effimg = self.copy_image(image)
      if self.effectimg is True:
        loginfo("Applying Effects")
        # https://www.reddit.com/r/django/comments/30ndh9/pil_getcolors_and_getpalette_trying_to_get_rgb/
        # https://pillow.readthedocs.io/en/stable/_modules/PIL/Image.html#effect_mandelbrot
        # ****** TODO: blend, composite, merge, effect_mandelbrot, effect_noise, linear_gradient, radial_gradient
        #self.effimg = image.effect_mandelbrot((800,600),(-2.0,-1.5,1.0,1.5),100)
        self.effimg = self.effimg.effect_spread(25)
      return self.effimg


    def size_image(self,image,resize=True):
      self.sizedimg = self.copy_image(image)
      if self.thumbnail is True:
        loginfo("Thumbnailing Image")
        self.sizedimg.thumbnail(self.thumbsize)
      if self.zoomed is True and self.thumbnail is not True:
        self.sizedimg = self.get_resized_img(self.sizedimg,(self.sizedimg.width * self.zoom,self.sizedimg.height * self.zoom))
        loginfo("Zoomed Image:",self.sizedimg)
      elif self.resize is True and resize is True and self.thumbnail is not True:
        self.sizedimg = self.get_resized_img_fit(self.sizedimg)
        loginfo("Sized Image:",self.sizedimg)
      return self.sizedimg


    def pil_image(self,image):
      if image.mode == "1": # bitmap image
        loginfo("Loading as BitmapImage ...")
        ImageFile.LOAD_TRUNCATED_IMAGES = False
        loginfo("ImageFile.LOAD_TRUNCATED_IMAGES",ImageFile.LOAD_TRUNCATED_IMAGES)
        try:
          self.pilimg = PIL.ImageTk.BitmapImage(image, foreground=self.color)
        except OSError as e:
          self.stauserrorlbl.config(text="Error: " + str(e))
          logwarn(e)
          if self.show_ui_error_messages is True:
            messagebox.showerror("File Error",e)
          if self.image_mode is False:
            self.log("File Error\n"+str(e)+"\n"+self.filenamepath)
          else:
            self.log("File Error\n"+str(e)+"\n"+self.image_name)
            ImageFile.LOAD_TRUNCATED_IMAGES = True
          self.pilimg = PIL.ImageTk.BitmapImage(image, foreground=self.color)
        finally:
          ImageFile.LOAD_TRUNCATED_IMAGES = self.load_trunc
      else:                       # photo image
        loginfo("Loading as PhotoImage ...")
        # https://www.programcreek.com/python/example/64885/PIL.ImageTk.PhotoImage
        ImageFile.LOAD_TRUNCATED_IMAGES = False
        loginfo("ImageFile.LOAD_TRUNCATED_IMAGES",ImageFile.LOAD_TRUNCATED_IMAGES)
        try:
          self.pilimg = PIL.ImageTk.PhotoImage(image)
        except OSError as e:
          self.stauserrorlbl.config(text="File Error: " + str(e))
          logwarn(e)
          if self.show_ui_error_messages is True:
            messagebox.showerror("File Error",e)
          if self.image_mode is False:
            self.log("File Error\n"+str(e)+"\n"+self.filenamepath)
          else:
            self.log("File Error\n"+str(e)+"\n"+self.image_name)
          ImageFile.LOAD_TRUNCATED_IMAGES = True
          self.pilimg = PIL.ImageTk.PhotoImage(image)
        finally:
          ImageFile.LOAD_TRUNCATED_IMAGES = self.load_trunc
      return self.pilimg


    # https://stackoverflow.com/questions/61456843/python-tkinter-change-how-to-change-cursor-without-the-use-of-canvas-widgets
    # https://pythonhosted.org/pyglet/programming_guide/changing_the_mouse_cursor.html
    @trace(1)
    # display should only deal with images not files, it is abstracted to the image level
    # TODO: lock display and changes to the images from other methods while slide show is going
    def display(self,image=None,resize=True,print_info=True):
      """ Display the image with selected filters """
      # https://www.geeksforgeeks.org/python-pil-image-convert-method/
      # TODO: pri=0;sev=0; change cursor and block (busy circle)
      # DONE: thumbnails, BAM! https://www.geeksforgeeks.org/python-pil-image-thumbnail-method/
      if image is not None:
        self.rawimg = image
      if self.rawimg is None:
        if self.canvas is not None:
          self.canvas.config(image='', bg=self.color)
        logwarn("There is no image to display!")
        # TODO: when we 'j' jack the desktop with no files loaded we hit this and a small grey square vertical rectangle appears, make that not happen
        return
      loginfo("Raw Image Width: {} Height: {}".format(self.rawimg.width,self.rawimg.height))
      if print_info is True: self.print_image_info(self.rawimg,
                                                     show_file=False,
                                                     test_images=False,
                                                     check_format_modes=False,
                                                     check_palette=False)
      loginfo("ImageFile.LOAD_TRUNCATED_IMAGES",ImageFile.LOAD_TRUNCATED_IMAGES)
      try:
        self.master.config(cursor="watch")
        ImageFile.LOAD_TRUNCATED_IMAGES = self.load_trunc
        image = self.rawimg
        image = self.apply_filters(image)
        image = self.apply_effects(image)
        # format file data as image data
        if self.show is True:
          image = self.size_image(image,resize=resize)
          image = self.pil_image(image)
          loginfo("PhotoImage: PILWidth",self.pilimg.width(),", PILHeight",self.pilimg.height())
          loginfo("PIL Image:",self.pilimg)
          if self.canvas is not None:
            #loginfo("Setting Image in Label via Config")
            if self.use_canvas is True:
              self.canvas.create_image(width=self.pilimg.width(), height=self.pilimg.height(), anchor=NE, image=self.pilimg)
            else:
              self.canvas.config(image=self.pilimg, bg=self.color, width=self.pilimg.width(), height=self.pilimg.height())
            #loginfo("Done Setting Image in Label via Config")
          else:
            loginfo("The Picture Frame is not Present!")
        elif self.muted is False: # only do this once after show is false
          self.canvas.config(image='', bg=self.color)
          loginfo("Muting")
          self.muted = True
        if self.desktop_mode is True:
          self.canvas.after(1,self.display_desktop)
      except Exception as e:
        exception(e)
      finally:
        self.master.config(cursor="arrow")


    @trace(3)
    def display_desktop(self):
      self.set_wallpaper_from_image(self.effimg,print_info=True)


    # https://www.codespeedy.com/get-the-basic-image-information-with-pillow-python/
    # TODO: https://stackoverflow.com/questions/4764932/in-python-how-do-i-read-the-exif-data-for-an-image
    # TODO: https://www.blog.pythonlibrary.org/2021/01/13/getting-gps-exif-data-with-python/
    @trace(3)
    def print_image_info(self,img,
                         show_file=True,
                         print_types=False,
                         test_images=False,
                         check_format_modes=False,
                         check_palette=False):
      # TIFF - RGBA, PNG - RGBA, GIF - P, JPEG - L, BMP  - P, BMP - 1,
      if print_types is True:
        if show_file is True:
          # Getting the filename of image
          print("Filename type",type(img.filename),"          : ",img.filename)
        # Getting the format of image
        print("Format type",type(img.format),"            : ",img.format)
        # Getting the mode of image
        print("Mode type",type(img.mode),"              : ",img.mode)
        # Getting the size of image
        print("Size type",type(img.size),"            : ",img.size)
        # Getting only the width of image
        print("Width type",type(img.width),"             : ",img.width)
        # Getting only the height of image
        print("Height type",type(img.height),"            : ",img.height)
        # Getting the color palette of image
        print("Image Palette type",type(img.palette),": ",img.palette)
        # Getting the info about image
        print("Image Info type",type(img.info),"       : ",img.info)
        # get band information
        bands = img.getbands()
        print("Bands type",type(bands),"           : ",bands)
      else:
        if show_file is True:
          # Getting the filename of image
          print("Filename      : ",img.filename)
        # Getting the format of image
        print("Format        : ",img.format) # JPEG, GIF, BMP, WEBP, PNG
        # Getting the mode of image
        print("Mode          : ",img.mode) # RGB, P, L, RGBA. 1
        # Getting the size of image
        print("Size          : ",img.size)
        # Getting only the width of image
        print("Width         : ",img.width)
        # Getting only the height of image
        print("Height        : ",img.height)
        # Getting the color palette of image
        print("Image Palette : ",img.palette)
        # Getting the info about image
        print("Image Info    : ",img.info)
        # get band information
        bands = img.getbands()
        print("Bands         : ",bands)
        exif = self.get_exif(img)
        if len(exif) > 0:
          print("Exif:",exif)
          #for x in exif:
          #  print("Exif:",x)
      if test_images is True:
        # do some checking to see what is what
        if img.format != "JPEG" and img.format != "BMP" and img.format != "PNG" and img.format != "WEBP"  and img.format != "GIF"  and img.format != "TIFF":
          logwarn("New FORMAT!")
        if img.mode != "RGBA" and img.mode != "RGB" and img.mode != "P" and img.mode != "L" and img.mode != "1":
            logwarn("New MODE!")
        if check_palette is True:
          if img.palette is not None:
            logwarn("Image has Palette") # does mode 'P' stand for Palette?
        if check_format_modes is True:
          if (img.format == "JPEG" and img.mode != "RGB") and (img.format == "JPEG" and img.mode != "L"):
            logwarn("New JPEG Mode!")
          if (img.format == "PNG" and img.mode != "RGB") and (img.format == "PNG" and img.mode != "RGBA") and (img.format == "PNG" and img.mode != "P"):
            logwarn("New PNG Mode!")
          if img.format == "TIFF" and img.mode != "RGBA":
            logwarn("New TIFF Mode!")
          if (img.format == "BMP" and img.mode != "RGB") and (img.format == "BMP" and img.mode != "P") and (img.format == "BMP" and img.mode != "1"):
            logwarn("New BMP Mode!")
          if img.format == "GIF" and img.mode != "P":
            logwarn("New GIF Mode!")
          if (img.format == "WEBP" and img.mode != "RGB") and (img.format == "WEBP" and img.mode != "RGBA"):
            logwarn("New WEBP Mode!")
        #if img.mode == 'P':
        #  pause()


    @trace(3)
    def print_video_info(self,cap,changes_only=False):
      # https://www.programcreek.com/python/example/70428/cv2.CAP_PROP_FRAME_WIDTH
      # https://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html#videocapture-get
      # https://stackoverflow.com/questions/11420748/setting-camera-parameters-in-opencv-python
      print("Current Timestamp:",cap.get(self.eCap.CV_CAP_PROP_POS_MSEC)) # CV_CAP_PROP_POS_MSEC
      print("Next Frame       :",cap.get(self.eCap.CV_CAP_PROP_POS_FRAMES)) # CV_CAP_PROP_POS_FRAMES
      if changes_only is False:
        print("Frame Width      :",cap.get(self.eCap.CV_CAP_PROP_POS_AVI_RATIO)) # CV_CAP_PROP_POS_AVI_RATIO
        print("Width            :",cap.get(self.eCap.CV_CAP_PROP_FRAME_WIDTH)) # CV_CAP_PROP_FRAME_WIDTH
        print("Height           :",cap.get(self.eCap.CV_CAP_PROP_FRAME_HEIGHT)) # CV_CAP_PROP_FRAME_HEIGHT
        print("FPS              :",cap.get(self.eCap.CV_CAP_PROP_FPS)) # CV_CAP_PROP_FPS
        print("FOURCC           :",cap.get(self.eCap.CV_CAP_PROP_FOURCC)) # CV_CAP_PROP_FOURCC
        print("#Frames          :",cap.get(self.eCap.CV_CAP_PROP_FRAME_COUNT)) # CV_CAP_PROP_FRAME_COUNT
        print("Mat Object Format:",cap.get(self.eCap.CV_CAP_PROP_FORMAT)) # CV_CAP_PROP_FORMAT
        print("Capture Mode     :",cap.get(self.eCap.CV_CAP_PROP_MODE)) # CV_CAP_PROP_MODE
        print("Brightness       :",cap.get(self.eCap.CV_CAP_PROP_BRIGHTNESS)) # CV_CAP_PROP_BRIGHTNESS
        print("Contrast         :",cap.get(self.eCap.CV_CAP_PROP_CONTRAST)) # CV_CAP_PROP_CONTRAST
        print("Saturation       :",cap.get(self.eCap.CV_CAP_PROP_SATURATION)) # CV_CAP_PROP_SATURATION
        print("Hue              :",cap.get(self.eCap.CV_CAP_PROP_HUE)) # CV_CAP_PROP_HUE
        print("Gain             :",cap.get(self.eCap.CV_CAP_PROP_GAIN)) # CV_CAP_PROP_GAIN
        print("Exposure         :",cap.get(self.eCap.CV_CAP_PROP_EXPOSURE)) # CV_CAP_PROP_EXPOSURE
        print("RGB Convert      :",cap.get(self.eCap.CV_CAP_PROP_CONVERT_RGB)) # CV_CAP_PROP_CONVERT_RGB
        print("Next Value       :",cap.get(self.eCap.CV_CAP_PROP_CONVERT_RGB+1)) # ?
        # unsupported re:https://stackoverflow.com/questions/11420748/setting-camera-parameters-in-opencv-python
        #print("White Balance    :",cap.get(self.eCap.CV_CAP_PROP_WHITE_BALANCE)) # CV_CAP_PROP_WHITE_BALANCE
        #print("Buffer Frames    :",cap.get(CV_CAP_PROP_BUFFERSIZE)) # CV_CAP_PROP_BUFFERSIZE
        #  only supported by DC1394 v 2.x backend re:https://stackoverflow.com/questions/11420748/setting-camera-parameters-in-opencv-python
        #print("The rest is only supported by DC1394 v 2.x backend currently")
        #print("Rectifictation   :",cap.get(self.eCap.CV_CAP_PROP_RECTIFICATION)) # CV_CAP_PROP_RECTIFICATION # note: only supported by DC1394 v 2.x backend currently
        #print("White Balance U  :",cap.get(cv2.CV_CAP_PROP_WHITE_BALANCE_U))  # note: only supported by DC1394 v 2.x backend currently
        #print("White Balance V  :",cap.get(cv2.CV_CAP_PROP_WHITE_BALANCE_V))  # note: only supported by DC1394 v 2.x backend currently
        #print("Rectification    :",cap.get(cv2.CV_CAP_PROP_RECTIFICATION))    # note: only supported by DC1394 v 2.x backend currently
        #print("ISO Speed        :",cap.get(cv2.CV_CAP_PROP_ISO_SPEED))        # note: only supported by DC1394 v 2.x backend currently


    @trace(3)
    def on_make_icons_from_image(self):
      self.make_icons_from_image()


    @trace(3)
    def square_image(self,img):
      if img.width > img.height:
        x = (img.width - img.height)/2
        y = 0
        length = img.height
        loginfo("New Size:: X:",x,"Y:",y,"Length:",length)
        return img.crop((x,0,length,length))
      elif img.height > img.width:
        x = 0
        y = (img.height - img.width)/2
        length = img.width
        loginfo("New Size:: X:",x,"Y:",y,"Length:",length)
        return img.crop((x,y,length,length))


    @trace(3)
    def make_icon_from_image(self,size,path,name):
      file = path + name + '_' + str(size) + 'x' + str(size) + '_Xbit.png'
      loginfo("Saving as",file)
      img = self.filtimg.copy()
      img = self.square_image(img)
      img = self.get_resized_img(img,(size,size))
      img.convert('RGBA')
      img.save(file)
      img.close()


    @trace(3)
    def make_icons_from_image(self):
      # lets make a tidy subfolder with unique folders for each time so this doesn't get messy
      # TODO: use resize, thumbs don't do exact sizes they just fit into the specified size
      path = self.module_path + "\\icons\\" + str(uuid.uuid4()) + "\\"
      if os.path.exists(path) is False:
        os.mkdir(path)
      self.make_icon_from_image(16,path,self.file_name)
      self.make_icon_from_image(32,path,self.file_name)
      self.make_icon_from_image(64,path,self.file_name)
      # verify square crop by not resizing
      img = self.filtimg.copy()
      img = self.square_image(img)
      img.convert('RGBA')
      file = path + self.file_name + '_' + str(img.width) + 'x' + str(img.height) + '_crop.png'
      img.save(file)
      img.close()
      # verify square crop via unmodified copy to compare
      img = self.filtimg.copy()
      img.convert('RGBA')
      file = path + self.file_name + '_' + str(img.width) + 'x' + str(img.height) + '_normal.png'
      img.save(file)
      img.close()


    @trace(3)
    def time_stamp(self):
      # https://strftime.org/
      return datetime.now().strftime("%Y%m%d_%H%M%S_%f")


    @trace(3)
    def log(self,*args,**kwargs):
      info = get_stack_frame_info(backtrack=3) # 3, get_stack_frame_info -> log -> trace -> caller
      loginfo("Module Path",self.module_path)
      path = self.module_path + "\\logs"
      loginfo("Log Path",path)
      if os.path.exists(path) is False:
        os.mkdir(path)
      logfile = ntpath.join(path,self.logfile)
      # https://www.guru99.com/reading-and-writing-files-in-python.html
      loginfo("Logfile is",logfile)
      file = open(logfile, 'a+')
      file.write("\n\r" + " ".join(map(str,args)) + "\n\r")
      file.write("in> "+info.function+" @ "+info.filename+", ln "+str(info.lineno)+"\n\r")
      file.close


    @trace(3)
    def open_file_dialog(self):
      filename = filedialog.askopenfilename()
      assert filename is not None, "filename is " + str(filename)
      f = os.path.abspath(filename)
      self.filenamepath = f.replace('/', '\\')
      self.root_directory = os.path.dirname(self.filenamepath)
      #self.get_file_path_info(self.filenamepath)
      if self.filenamepath is not None and self.filenamepath != "":
        self.isources = 0
        self.sources.clear()
        self.open_file(self.filenamepath,append=True)


    @trace(3)
    def open_file(self,file,append=False,print_info=True):
      self.statusinfolbl.config(text='')
      self.stauserrorlbl.config(text='')
      self.is_GIF_file = False
      if append is True:
        self.ordered_sources.append(file)
        if len(self.ordered_sources) > 1:
          self.enable()
        else:
          self.disable()
      self.get_file_path_info(file)
      if self.file_ext is not None:
        self.close_video_file()
        if self.file_ext.lower() in self.supported_image_extensions:
          self.open_image_file(file)
        elif self.file_ext.lower() in self.supported_video_extensions:
          return self.open_video_file(file)
        else:
          logwarn("Extension:",self.file_ext,", File:",file,"is not a supported media type")
          self.stauserrorlbl.config(text="Extension: " + self.file_ext + ", File: " + file + " is not a supported media type")
      else:
        logerror("File",file,"has no extension and is not supported")
        self.stauserrorlbl.config(text="File " + file + " has no extension and is not supported")


    @trace(3)
    def open_video_file(self,file,print_info=True):
      # TODO: close the capture when done
      assert file is not None, "File is " + str(file)
      self.close_video_file()
      loginfo("Opening Video Capture")
      if self.showfile is True: print(file)
      try:
        if self.privacy is True:
          self.master.title("Viewing in Privacy Mode")
        else:
          self.master.title("Viewing  " + file)
        # https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html
        self.vidcap = cv2.VideoCapture(file)
        # https://stackoverflow.com/questions/18954889/how-to-process-images-of-a-video-frame-by-frame-in-video-streaming-using-openc
        #while not cap.isOpened():
        #  cap = cv2.VideoCapture("./out.mp4")
        #  cv2.waitKey(1000)
        #  print "Wait for the header"
        if self.vidcap.isOpened() is False:
          self.vidcap.open()
        self.filenamepathlbltext.set(file)
        if print_info is True:
          self.print_video_info(self.vidcap)
        if self.tb_frametool not in self.tb_widgets:
          self.toggle_frames_tool(toggle=False,value=True)
        self.process_cv_frame()
      except Exception as e:
        self.stauserrorlbl.config(text="Error: "+ str(e))
        exception(e)


    @trace(3)
    def close_video_file(self):
      if self.vidcap is not None:
        loginfo("Closing Video Capture")
        self.vidcap.release()
        self.vidcap = None


    @trace(3)
    def clear_contents(self):
      self.isources = 0
      self.sources.clear()


    @trace(3)
    def close_images(self):
      if self.rawimg is not None:
        logverb("Closing Previous Raw Image File")
        self.rawimg.close()
        self.rawimg = None
      if self.filtimg is not None:
        logverb("Closing Previous Filtered Image File")
        self.filtimg.close()
        self.filtimg = None
      if self.sizedimg is not None:
        logverb("Closing Previous Sized Image File")
        self.sizedimg.close()
        self.sizedimg = None



    @trace(3)
    def open_image(self,filepathname,peek=False): # TODO: try out peek on a trial basis
      self.is_GIF_file = False
      img = None
      self.close_images()
      #self.file_name,self.file_ext = self.get_file_name_ext(filepathname)
      if self.file_ext.upper() == 'B64': # special case needs some prep
          img = self.open_base64(filepathname,peek=peek)
      else:
        try:
          logverb("Opening Image File")
          img = PIL.Image.open(filepathname)
        except OSError as e:
          if peek == False:
            logwarn(e)
            if self.show_ui_error_messages is True:
              messagebox.showerror("File Error",e)
            self.stauserrorlbl.config(text="Error: "+ str(e))
            if self.image_mode is False:
              self.log("File Error\n"+str(e)+"\n"+ntpath.join(self.root_directory,filepathname)+"\n")
            else:
              self.log("File Error\n"+str(e)+"\n"+self.image_name+"\n")
          try:
            logverb("Opening Image File")
            img = PIL.Image.open(filepathname)
          except Exception as e:
            if peek == False:
              exception(e)
              if self.show_ui_error_messages is True:
                messagebox.showerror("File Error",e)
              self.stauserrorlbl.config(text="Error: "+ str(e))
              if self.image_mode is False:
                self.log("File Error\n"+str(e)+"\n"+ntpath.join(self.root_directory,filepathname))
              else:
                self.log("File Error\n"+str(e)+"\n"+self.image_name)
            img = None
        if img is None:
          img = self.get_resource_image()
      return img


    @trace(3)
    def open_base64(self,filepathname,peek=False):
      try:
        #b64 = base64.encodebytes(open(file,"rb").read()) # read in image file and encode, need in save
        loginfo("Open Base 64 Encoded Data File ->",filepathname)
        file = open(filepathname, 'r')
        self.base64data = file.read()
        file.close()
        #self.get_file_path_info(filepathname)
        loginfo("Base:",os.path.basename(self.file_name),", Ext:",self.file_ext)
        filename,ext = self.get_file_name_ext(self.file_name) # get inner file + extension
        if ext is not None:
          loginfo(os.path.basename(filename) + "_" + ext + "_b64='''\\\n" + self.base64data + "'''")
        else:
          loginfo(os.path.basename(filename) + "_" + "unk" + "_b64='''\\\n" + self.base64data + "'''")
        encoded_bytes = base64.b64decode(self.base64data.encode())
        io_data = io.BytesIO(encoded_bytes)
        return Image.open(io_data)
      except Exception as e:
        if peek is False:
          self.stauserrorlbl.config(text="File Error: "+ str(e))
          logwarn(e)
          self.log("File Error\n"+str(e)+"\n"+ntpath.join(self.root_directory,filepathname))
          return self.get_resource_image()
      return None


    # https://www.codespeedy.com/get-the-basic-image-information-with-pillow-python/
    # https://pillow.readthedocs.io/en/5.2.x/reference/plugins.html#PIL.GifImagePlugin.GifImageFile.n_frames
    @trace(3)
    def open_image_file(self,filename,print_info=True):
      assert filename is not None, "filename is " + str(filename)
      try:
        if self.showfile is True:
          print(filename)
        #self.file_name,self.file_ext = self.get_file_name_ext(filename)
        if self.privacy is True:
          self.master.title("Viewing in Privacy Mode")
        else:
          self.master.title("Viewing  " + filename)
        self.rawimg = self.open_image(filename)
        if self.rawimg is not None:
          self.filenamepathlbltext.set(filename)
          # if print_info is True: self.print_image_info(self.rawimg,
                                                       # show_file=False,
                                                       # test_images=False,
                                                       # check_format_modes=False,
                                                       # check_palette=False)
          if self.debug is True: logverb("Call Display in open_image_file")
          logverb("Displaying Next Image File")
          self.display()
          #self.num_page=0
          #if self.rawimg.n_frames > 0: self.num_page = 1
          # TODO: pri=0;sev=0; handle no n_frames opening .jpg when display is not called by considering design impact
          # TODO: pri=0;sev=0; when a GIF is loaded display the GIFframes tool, get n_frames and display frame/n_frames and vice versa
          if self.rawimg.format == 'GIF':
            self.is_GIF_file = True
            if self.tb_frametool not in self.tb_widgets:
              self.toggle_frames_tool(toggle=False,value=True)
              #self.framecntr.set(str(self.rawimg.tell()) + "/" +  str(self.rawimg.n_frames))
              self.frame = 0
              self.framecntr.set(str(self.frame+1) + "/" + str(self.rawimg.n_frames))
          else:
            if self.tb_frametool in self.tb_widgets:
              self.toggle_frames_tool(toggle=False,value=False)
          if self.toolbar is not None: self.savebtn['state'] = NORMAL
        else:
          logwarn("Failed to open", filename, "Image is Null")
          self.rawimg = self.get_resource_image()
      except Exception as e:
        self.stauserrorlbl.config(text="File Error: "+ str(e))
        exception(e)
        self.log("File Error\n"+str(e)+"\n"+ntpath.join(self.root_directory,filename))
        self.close_images()
        self.rawimg = self.get_resource_image()


    @trace(3)
    def process_input_path(self,path):
      self.root_directory = os.path.dirname(path)
      if self.root_directory is not None:
        return True
      return False


    @trace(3)
    def process_input_dir(self,directory):
      if directory[1] == ':': # if a drive letter path
        if directory[-2] != ':': # dont strip root
          if list(directory)[-1] == '\\' or list(directory)[-1] == '/':
            directory = directory.rstrip('\\/')
      else:
        logwarn("Path is not a local or recognizable path!")
      assert directory is not None, "directory is " + str(directory)
      if directory is not None and directory != "":
          self.root_directory = directory
          return True
      else:
        logwarn("Directory is Empty! No Files to Display")
      return False


    @trace(3)
    def open_directory_dialog(self):
      d = filedialog.askdirectory()
      if d is not None and d != '':
        directory = d.replace('/', '\\')
        loginfo("Search Directory is", directory)
        self.root_directory = directory
        #self.filenamepath = os.path.abspath(arg)
        #self.root_directory = os.path.dirname(self.filenamepath)
        #self.get_file_path_info(self.filenamepath)
        if self.process_input_dir(directory) is True:
          self.open_files(directory)


    @trace(3)
    def open_files(self,directory):
      # TODO: pri=0;sev=0; if there are no files don't enable the app
      # TODO: pri=0;sev=0; parse any trailing backslashes, it still works if there is on but it doesn't look clean when display with '\\'
      # TODO: https://stackoverflow.com/questions/9770668/scramble-python-list
      # https://docs.python.org/3/library/random.html
      # if its not a root folder. E.g. c:\. also isn't a network path. E.g. \\
      self.sources.clear()
      self.isources  = 0
      # https://blog.hubspot.com/insiders/different-types-of-image-files
      # raw formats - cr2,crw,nef,pef
      iext = self.supported_image_extensions + self.supported_video_extensions
      if self.showfile is True: print("Scanning for",iext,"\nrecursively in",directory, "...")
      #xext = ['ini','db','wmv','mpeg','avi','txt','mpg','mp4','zip','mpa','ram','flv','rm','asf','mov','asx','divx','mswmm','doc','pdf','webm'] # just eliminating files for now to test what it can handle
      # TODO: pri=0;sev=0; option for dir or tree (/s basically)
      filtered = []
      # TODO: crawltree returning filenames that don't have extensions when iext specified, looks like my fix didn't work
      self.ordered_sources = crawltree(directory,
                                      iext=iext,
                                      xfiles=['_WARNING.jpg'],
                                      showfiles=False,
                                      no_dirs=True,
                                      quiet=True,
                                      verbose=False,
                                      pause_on_error=False,
                                      debug=self.debug)

      if len(self.ordered_sources) > 0:
        #loginfo("Sources:",self.sources)
        self.root_directory = directory
        self.sources = self.ordered_sources # set initially to ordered
        # set shuffle sources
        self.shuffled_sources.clear()
        self.shuffled_sources = self.ordered_sources[:]
        random.shuffle(self.shuffled_sources)
        self.ishuffled_sources = 0
        if self.sortbydate is True:
          self.ordered_sources.sort(key=self.sort_files_by_date,reverse=self.reverse_sort)
        # TODO: shuffle sources
        # TODO: add way to avoid smaller size images, below temp code show sample getting image information
        # TODO: add portait or landscape only mode, the below temp code was testing this out, use that to get image information
        if len(self.ordered_sources) > 1:
          self.enable()
        if len(self.ordered_sources) > 0:
          self.open_file(ntpath.join(self.root_directory,self.sources[self.isources]))
      else:
        self.stauserrorlbl.config(text="Files Not Found: There were no images found in" + directory)
        if self.show_ui_error_messages is True:
          messagebox.showerror("Files Not Found!","There were no images found in" + directory)


    def sort_files_by_date(self,file):
      return os.path.getmtime(os.path.join(self.root_directory,file))


    @trace(3)
    def save_image_to_file(self,filename):
      # TODO: update for B64 file format
      assert filename is not None, "filename is " + str(filename)
      loginfo("Saving ...",filename)
      try:
        # https://www.geeksforgeeks.org/python-pil-image-save-method/
        self.filtimg.save(filename) # the extension tells it what to save as
      except Exception as e:
        loginfo("Failed to Save",filename)
        exception(e)
        self.log("File Save Error\n"+str(e)+"\n"+filepathname)


    @trace(3)
    def save_file_as_dialog(self):
      if self.file_ext is not None and self.file_ext.upper() == 'B64':
        filename,extension = self.get_file_name_ext(self.file_name)
        if extension is not None:
          filenameext = str(filename) + '.' + extension
        else:
          filenameext = str(filename)
      else:
        # generate a unique name for quick save and easy edit
        filename = uuid.uuid4()
        if self.file_ext is not None:
          filenameext = str(filename) + '.' + self.file_ext
        else:
          filenameext = str(filename)
      # TODO: .riff? (resource interchange file format)
      filenameext = filedialog.asksaveasfilename(title = "Save File As",
                                                defaultextension=".jpg",
                                                initialfile=filenameext,
                                                filetypes=(("Jpeg Files","*.jpg"),
                                                           ("Ping Files","*.png"),
                                                           ("Jpeg Files","*.jpeg"),
                                                           ("TIFF Files","*.tiff"),
                                                           ("GIF Files","*.gif"),
                                                           ("Bitmap Files","*.bmp"),
                                                           ("Portable Pixelmap","*.ppm"),
                                                           ("Base64 Encoded","*.b64"),
                                                           ("WebP Files","*.webp"),       # https://en.wikipedia.org/wiki/WebP (pronounced Weppy)
                                                           ("WebM Files","*.webm"),
                                                           ("Icon Files","*.ico")))
      assert filenameext is not None, "File Name is " + str(filenameext)
      if filenameext is not None and filenameext != '':
        filename,extension = self.get_file_name_ext(filenameext)
        if extension is not None and extension.upper() == 'B64':
          if self.file_ext.upper() == 'B64':
            # save 'data' to file? or encode again?
            if self.base64data is not None:
              file = open(filenameext,'w')
              file.write(self.base64data)
              file.close()
            else:
              logerror("There is no Base64 encoded data to write!")
          else:
            if self.filtimg is not None:
              # graphic image needs encoding
              file = open(filenameext,'w')
              file.write(base64data.encodebytes(self.filtimgg))
              file.close()
            else:
              logerror("There is no image to encode and write to file!")
        else:
          if self.filtimg is not None:
            self.save_image_to_file(filenameext)
          else:
            logerror("There is no image to write to file!")


    # https://stackoverflow.com/questions/8600161/executing-periodic-actions-in-python
    @trace(3)
    def start_slideshow(self):
      # TODO: add countdown timer to next slide in status
      if self.timer is None:
        if len(self.sources) > 0:
          currtime = datetime.now()
          # https://www.mytecbits.com/internet/python/addition-and-subtraction-of-time
          newtime = currtime + timedelta(seconds=self.interval)
          # newtime.strftime("%S.%f") # E.g. 44.641333 # retaining example of formatting
          # TODO: Starting slide show maybe?
          loginfo("Next slide in",self.interval,"seconds @",newtime)
          self.showbtn.config(text="Stop")
          # reset isources if we stopped at the end otherwise it won't restart
          if self.isources >= len(self.sources) - 1:
            self.isources  = -1
          self.timer = threading.Timer(self.interval, self.show_slide)
          self.timer.daemon = True
          self.timer.start()
      else:
        self.stop_slideshow()


    @trace(3)
    def show_slide(self):
      # TODO: timing for slides like how close to when it was scheduled did it actually display, rendering comes after the timer so the slide will be delayed the rendering time. I want to see this information and catch any multiple timers or times that weren't scheduled
      # TODO: blending previous and next images in various wipes
      if self.timer is not None:
        self.next_file()
        if self.timer is not None:
          # https://www.mytecbits.com/internet/python/addition-and-subtraction-of-time
          newtime = datetime.now() + timedelta(seconds=self.interval)
          loginfo("Next slide in",self.interval,"seconds @",newtime)
          self.timer = threading.Timer(self.interval, self.show_slide)
          self.timer.daemon = True
          self.timer.start()


    @trace(3)
    def on_space(self,event):
      loginfo("on_space")
      if self.timer == None:
        self.start()
      else:
        self.stop()


    @trace(3)
    def on_up(self,event):
      self.master.geometry('+{}+{}'.format(self.master.winfo_x(), self.master.winfo_y()-1))


    @trace(3)
    def on_down(self,event):
      self.master.geometry('+{}+{}'.format(self.master.winfo_x(), self.master.winfo_y()+1))


    @trace(3)
    def on_left(self,event):
      self.master.geometry('+{}+{}'.format(self.master.winfo_x()-1, self.master.winfo_y()))


    @trace(3)
    def on_right(self,event):
      self.master.geometry('+{}+{}'.format(self.master.winfo_x()+1, self.master.winfo_y()))


    @trace(3)
    def on_up_fast(self,event):
      self.master.geometry('+{}+{}'.format(self.master.winfo_x(), self.master.winfo_y()-10))


    @trace(3)
    def on_down_fast(self,event):
      self.master.geometry('+{}+{}'.format(self.master.winfo_x(), self.master.winfo_y()+10))


    @trace(3)
    def on_left_fast(self,event):
      self.master.geometry('+{}+{}'.format(self.master.winfo_x()-10, self.master.winfo_y()))


    @trace(3)
    def on_right_fast(self,event):
      self.master.geometry('+{}+{}'.format(self.master.winfo_x()+10, self.master.winfo_y()))


    @trace(3)
    def on_upper_left(self,event):
      self.master.geometry('+{}+{}'.format(0, 0))


    @trace(3)
    def on_lower_right(self,event):
      self.master.geometry('+{}+{}'.format(self.master.winfo_screenwidth(), self.master.winfo_screenheight()))


    @trace(3)
    def on_center(self,event):
      # Gets the requested values of the height and widht.
      windowWidth = self.master.winfo_reqwidth()
      windowHeight = self.master.winfo_reqheight()
      loginfo("Width:",windowWidth,"Height:",windowHeight)
      # Gets both half the screen width/height and window width/height
      x = int(self.master.winfo_screenwidth()/2 - windowWidth/2)
      y = int(self.master.winfo_screenheight()/2 - windowHeight/2)
      # Positions the window in the center of the page.
      self.master.geometry("+{}+{}".format(x, y))


    @trace(3)
    def on_increase_interval(self,event):
      # TODO: show interval in seconds on screen briefly when changing, make sure it's visible in widget mode and tool (small font for latter)
      self.interval = self.interval / self.interval_incdec
      loginfo("Interval:",self.interval)
      if self.picture_frame is not None: self.picture_frame.focus_set()
      if self.timer is not None:
        self.timer.cancel()
        newtime = datetime.now() + timedelta(seconds=self.interval)
        loginfo("Next slide in",self.interval,"seconds @",newtime)
        self.timer = threading.Timer(self.interval, self.show_slide)
        self.timer.daemon = True
        self.timer.start()


    @trace(3)
    def on_decrease_interval(self,event):
      self.interval = self.interval * self.interval_incdec
      loginfo("Interval:",self.interval)
      if self.picture_frame is not None: self.picture_frame.focus_set()
      if self.timer is not None:
        self.timer.cancel()
        newtime = datetime.now() + timedelta(seconds=self.interval)
        loginfo("Next slide in",self.interval,"seconds @",newtime)
        self.timer = threading.Timer(self.interval, self.show_slide)
        self.timer.daemon = True
        self.timer.start()


    @trace(3)
    def set_interval(self,interval):
      self.interval = interval
      loginfo("Interval:",self.interval)


    @trace(3)
    def on_home(self,event):
      self.go_to_first_slide()


    @trace(3)
    # TODO: new function to clear out slide history and reset to home since go_to_first_slide doesn't do this anymore
    def go_to_first_slide(self):
      self.stop()
      if self.random is True and len(self.history):
        self.isources = self.history[0]
        self.ihistory = 0
      else:
        self.isources = 0
      if len(self.sources) > 0:
        self.open_file(ntpath.join(self.root_directory,self.sources[self.isources]))


    @trace(3)
    def on_end(self,event):
      self.go_to_last_slide()


    @trace(3)
    def go_to_last_slide(self):
      self.stop()
      if self.random is True and len(self.history):
        self.isources = self.history[-1]
        self.ihistory = len(self.history)-1
      else:
        self.isources = len(self.sources)-1
      if len(self.sources) > 0:
        self.open_file(ntpath.join(self.root_directory,self.sources[self.isources]))


    @trace(3)
    def on_page_down(self,event):
      #if self.isources < len(self.sources):
      self.go_to_next_directory()


    @trace(3)
    def go_to_next_directory(self):
      loginfo("Advancing to the next directory")
      loginfo("Next Image: isources =",self.isources,",repeat =",self.repeat,",len(sources) =",len(self.sources))
      if self.random is True:
        logwarn("Next Directory access not valid in Random Mode")
      else:
        # get temp index in case file isn't opened
        index = self.isources
        count = 0
        currentdir = os.path.split(self.sources[index])[0]
        loginfo("Current Dir is",currentdir)
        while index < len(self.sources):
          loginfo("Scanning... Index:",index,"File:",self.sources[index])
          if os.path.split(self.sources[index])[0] != currentdir:
            loginfo("Found! ->",os.path.split(self.sources[index])[0])
            self.open_file(ntpath.join(self.root_directory,self.sources[index]))
            self.isources = index
            break
          index = index + 1
          if self.repeat is True and index == len(self.sources):
            index = 0
          count = count + 1
          if count >= len(self.sources):
            loginfo("Directory Not Found!")
            break # only check all entries once


    @trace(3)
    def on_page_up(self,event):
      #if self.isources > 0:
      self.go_to_prev_directory()


    # TODO: random slide show that goes through the directories and shows one picture from each randomly or sequentially
    @trace(3)
    def go_to_prev_directory(self):
      loginfo("Previous Dir: isources =",self.isources,",repeat =",self.repeat,",len(sources) =",len(self.sources))
      if self.random is True:
        logwarn("Previous Directory access not valid in Random Mode")
      else:
        # DONE: consider changing behaviour on previous to go to top of current directory first before the previous one. Next is fine I think as I don't see going to the last image in the directory to be useful. The first is because it is the image that will be associated with the directory and what the user will see when scrolling through the directories and going to the start of the directory is a needed function. The feel was off too, when I went up it felt like i should be going to the top of that directory and that was what I was expecting and needed as well.
        # get temp index in case file isn't opened
        index = self.isources
        count = 0
        cindex = index
        folder = path = os.path.split(self.sources[index])[0]
        loginfo("Current Index:",cindex,"Folder:",folder)

        while index > -1 and index < len(self.sources):
          loginfo("Scanning... Index:",index,"File:",self.sources[index])
          if os.path.split(self.sources[index])[0] != path or (index == 0 and self.repeat is False):
            if cindex <= index + 1 and index != 0:
              path = os.path.split(self.sources[index])[0]
              loginfo("Continuing to the top of",path)
            else:
              if index != 0: index = (index + 1) % len(self.sources)
              loginfo("Found! ->",self.sources[index])
              self.open_file(ntpath.join(self.root_directory,self.sources[index]))
              self.isources = index
              break
          index = index - 1
          if self.repeat is True and index == -1:
            index = len(self.sources)-1
          count = count + 1
          if count >= len(self.sources):
            loginfo("Directory Not Found!")
            break # only check all entries once


    @trace(3)
    def on_img_orig(self,event):
      self.img_origional()


    @trace(3)
    def img_origional(self):
      loginfo("Resize Off")
      self.resize = False
      self.zoomed = False
      self.thumbnail = False
      if self.toolbar is not None: self.resizebtn.config(text="Scale")
      self.filtimg = self.rawimg
      if self.debug is True: loginfo("Call Display in on_img_orig")
      self.num_page=0
      self.hide_statusbar()
      self.display()


    @trace(3)
    def on_img_resize(self,event):
      self.img_resize()


    @trace(3)
    def img_resize(self):
      loginfo("Resize On")
      self.resize = True
      self.zoomed = False
      self.thumbnail = False
      if self.toolbar is not None: self.resizebtn.config(text="Size")
      # DONE: status bar should not show up if F2 was pressed
      if self.widgets_on is True:
        self.show_statusbar()
      if self.rawimg is not None:
        if self.debug is True: loginfo("Call Display on_img_resize")
        self.display()


    @trace(3)
    def on_toggle_thumbnail(self,event):
      self.toggle_thumbnail()


    @trace(3)
    def toggle_thumbnail(self,toggle=True,value=True):
      # DONE: thumnail is corrupting main image somehow, fix this. Its not 100% repro but will repro easy, just toggle resize, orig and thumb
      if toggle is False:
        self.thumbnail = value
      else:
        self.thumbnail = not self.thumbnail
      if self.thumbnail is True:
        loginfo("Thumnail ON")
      else:
        loginfo("Thumnail OFF")
      self.display()


    @trace(3)
    def on_toggle_resize(self,event):
      self.toggle_resize()


    @trace(3)
    def toggle_resize(self,toggle=True,value=True):
      if toggle is False:
        self.resize = value
      else:
        self.resize = not self.resize
      if self.resize is True or self.thumbnail is True:
        self.img_resize()
      else:
        self.img_origional()


    @trace(5)
    def on_window_resize(self, event):
      if self.pilimg is not None:
        #loginfo("State",self.master['state'])
        logspew(self.seperator)
        #if self.debug is True: loginfo("Width",self.master.winfo_width(),"Height",self.master.winfo_height())
        if self.debug is True: logspew("Event",event)
        logspew("Image  width:",self.pilimg.width(),"Image  height:",self.pilimg.height())
        logspew("Window width:",self.display_width(),"Window height:",self.display_height())
        logspew("Root   width:",self.master.winfo_width(),"Root   height:",self.master.winfo_height())
        logspew("Screen width:",self.master.winfo_screenwidth(),"Screen height:",self.master.winfo_screenheight())
        if self.resize is True and self.thumbnail is not True:
          if self.pilimg.width() <= self.display_width() and self.pilimg.height() <= self.display_height() and \
            (self.pilimg.width() == self.display_width() or self.pilimg.height() == self.display_height()):
              pass
          else:
            logwarn("Call Display on window_resize")
            self.display()
          #if self.pilimg.width() > self.display_width() or self.pilimg.height() > self.display_height() or \
          #  (self.pilimg.width() != self.display_width() and self.pilimg.height() != self.display_height()):
          #  if self.debug is True: logverb("Call Display on window_resize")
          #  self.display()
        logspew(self.seperator)


    @trace(3)
    def on_clear_selected_filters(self,event):
      self.clear_selected_filters()


    @trace(3)
    def clear_selected_filters(self):
      loginfo("Clear All Filters (except privacy filter)")
      self.filterimg = False
      self.filterbtn.config(text='Raw')
      self.grayscale = False
      self.blur = False
      self.contour = False
      self.detail = False
      self.enhance = False
      self.emboss = False
      self.edges = False
      self.sharpen = False
      self.smooth = False
      self.smooth_more = False
      self.selected_filters.clear()
      self.display()


    @trace(3)
    def on_toggle_filters(self,event):
      self.toggle_filters()


    @trace(3)
    def toggle_filters(self,toggle=True,value=True):
      if toggle is False:
        self.filterimg = value
      else:
        self.filterimg = not self.filterimg
      if self.filterimg is True:
        loginfo("Filter On")
        self.filterbtn.config(text='Fltrd')
      else:
        loginfo("Filter Off")
        self.filterbtn.config(text='Raw')
      self.display()


    @trace(3)
    def on_toggle_effects(self,event):
      self.toggle_effects()


    @trace(3)
    def toggle_effects(self,toggle=True,value=True):
      if toggle is False:
        self.effectimg = value
      else:
        self.effectimg = not self.effectimg
      if self.effectimg is True:
        loginfo("Effect On")
        #self.filterbtn.config(text='Fltrd')
      else:
        loginfo("Effect Off")
        #self.filterbtn.config(text='Raw')
      self.display()


    @trace(3)
    def on_toggle_grayscale(self,event):
        self.toggle_grayscale()


    # https://appdividend.com/2020/06/22/how-to-convert-pil-image-to-grayscale-in-python/
    # https://www.geeksforgeeks.org/python-pil-imageops-greyscale-method/
    @trace(3)
    def toggle_grayscale(self,toggle=True,value=True):
      if toggle is False:
        self.grayscale = value
      else:
        self.grayscale = not self.grayscale
      if self.grayscale is True:
        loginfo("Grayscale On")
      else:
        loginfo("Grayscale Off")
      self.display()



    @trace(3)
    def on_toggle_privacy(self,event):
        self.toggle_privacy()


    @trace(3)
    def toggle_privacy(self,toggle=True,value=True):
      if toggle is False:
        self.privacy = value
      else:
        self.privacy = not self.privacy
      if self.privacy is True:
        loginfo("Privacy On")
        if len(self.sources):
          self.master.title("Viewing in Privacy Mode")
      else:
        loginfo("Privacy Off")
        if len(self.sources):
          self.master.title("Viewing  " + self.sources[self.isources])
      self.display()


    @trace(3)
    def on_toggle_blur(self,event):
        self.toggle_blur()


    @trace(3)
    def toggle_blur(self,toggle=True,value=True):
      if toggle is False:
        self.blur = value
      else:
        self.blur = not self.blur
      if self.blur is True:
        self.filterimg = True
        self.selected_filters.append(ImageFilter.GaussianBlur(radius=1))
        loginfo("Blur On")
      else:
        if ImageFilter.GaussianBlur(radius=1) in self.selected_filters:
          self.selected_filters.remove(ImageFilter.GaussianBlur(radius=1))
          loginfo("Blur Off")
      self.display()


    @trace(3)
    def on_toggle_contour(self,event):
        self.toggle_contour()


    @trace(3)
    def toggle_contour(self,toggle=True,value=True):
      if toggle is False:
        self.contour = value
      else:
        self.contour = not self.contour
      if self.contour is True:
        self.filterimg = True
        self.selected_filters.append(ImageFilter.CONTOUR)
        loginfo("Contour On")
      else:
        #if len(self.selected_filters) <= 0: self.filterimg = False
        if ImageFilter.CONTOUR in self.selected_filters:
          self.selected_filters.remove(ImageFilter.CONTOUR)
          loginfo("Contour Off")
      self.display()


    @trace(3)
    def on_toggle_detail(self,event):
        self.toggle_detail()


    @trace(3)
    def toggle_detail(self,toggle=True,value=True):
      if toggle is False:
        self.detail = value
      else:
        self.detail = not self.detail
      if self.detail is True:
        self.filterimg = True
        self.selected_filters.append(ImageFilter.DETAIL)
        loginfo("Detail On")
      else:
        #if len(self.selected_filters) <= 0: self.filterimg = False
        if ImageFilter.DETAIL in self.selected_filters:
          self.selected_filters.remove(ImageFilter.DETAIL)
          loginfo("Detail Off")
      self.display()


    @trace(3)
    def on_toggle_enhance(self,event):
        self.toggle_enhance()


    @trace(3)
    def toggle_enhance(self,toggle=True,value=True):
      if toggle is False:
        self.enhance = value
      else:
        self.enhance = not self.enhance
      if self.enhance is True:
        self.filterimg = True
        self.selected_filters.append(ImageFilter.EDGE_ENHANCE)
        loginfo("Enhance On")
      else:
        #if len(self.selected_filters) <= 0: self.filterimg = False
        if ImageFilter.EDGE_ENHANCE in self.selected_filters:
          self.selected_filters.remove(ImageFilter.EDGE_ENHANCE)
          loginfo("Enhance Off")
      self.display()


    @trace(3)
    def on_toggle_enhance_more(self,event):
        self.toggle_enhance_more()


    @trace(3)
    def toggle_enhance_more(self,toggle=True,value=True):
      if toggle is False:
        self.enhance_more = value
      else:
        self.enhance_more = not self.enhance_more
      if self.enhance_more is True:
        self.filterimg = True
        self.selected_filters.append(ImageFilter.EDGE_ENHANCE_MORE)
        loginfo("Enhance More On")
      else:
        #if len(self.selected_filters) <= 0: self.filterimg = False
        if ImageFilter.EDGE_ENHANCE_MORE in self.selected_filters:
          self.selected_filters.remove(ImageFilter.EDGE_ENHANCE_MORE)
          loginfo("Enhance More Off")
      self.display()


    @trace(3)
    def on_toggle_emboss(self,event):
        self.toggle_emboss()


    @trace(3)
    def toggle_emboss(self,toggle=True,value=True):
      if toggle is False:
        self.emboss = value
      else:
        self.emboss = not self.emboss
      if self.emboss is True:
        self.filterimg = True
        self.selected_filters.append(ImageFilter.EMBOSS)
        loginfo("Emboss On")
      else:
        if ImageFilter.EMBOSS in self.selected_filters:
          self.selected_filters.remove(ImageFilter.EMBOSS)
          loginfo("Emboss Off")
      self.display()


    @trace(3)
    def on_toggle_edges(self,event):
        self.toggle_edges()


    @trace(3)
    def toggle_edges(self,toggle=True,value=True):
      if toggle is False:
        self.edges = value
      else:
        self.edges = not self.edges
      if self.edges is True:
        self.filterimg = True
        self.selected_filters.append(ImageFilter.FIND_EDGES)
        loginfo("Find Edges On")
      else:
        if ImageFilter.FIND_EDGES in self.selected_filters:
          self.selected_filters.remove(ImageFilter.FIND_EDGES)
          loginfo("Find Edges Off")
      self.display()


    @trace(3)
    def on_new_filter(self,event):
        self.new_filter(maximum=10)


    @trace(3)
    def new_filter(self,maximum=10,reset=True):
      self.filterimg = True
      self.edit_filter_mode = True
      if reset is True:
        self.selected_filters.clear()
      # min 2 filters or it's not a new filter unless it is aggregate as we are building
      # for single filters use 'add' command
      minimum = 2
      if maximum < 1: maximum = 1
      if maximum == 1: minimum = 1
      numfilters = random.randint(minimum,maximum)
      loginfo("Range 0 to", numfilters)
      for i in range(0,numfilters):
      # https://docs.python.org/3/library/random.html
      # https://pynative.com/python-random-choice/
        self.selected_filters.append(random.choice(list(self.filters.values())))
      loginfo("New Filters are", self.selected_filters)
      #if reset is True:
      #  self.filter_history.append(self.selected_filters)
      #else:
      #  ifilter_history = len(self.filter_history)
      #  self.filter_history[ifilter_history](self.selected_filters)
      #loginfo("Filter History", self.filter_history)
      #ifilter_history = len(self.filter_history)
      self.display()


    @trace(3)
    def on_new_aggregate_filter(self,event):
        self.new_aggregate_filter()


    @trace(3)
    def new_aggregate_filter(self):
      self.new_filter(maximum=1,reset=False)


    @trace(3)
    def on_toggle_test_flag(self,event):
        self.toggle_test_flag()


    @trace(3)
    def toggle_test_flag(self,toggle=True,value=True):
      if toggle is False:
        self.test = value
      else:
        self.test = not self.test
      if self.test is True:
        self.filterimg = True
        loginfo("Test Flag On")
      else:
        loginfo("Test Flag Off")
      self.display()


    @trace(3)
    def on_toggle_sharpen(self,event):
        self.toggle_sharpen()


    @trace(3)
    def toggle_sharpen(self,toggle=True,value=True):
      if toggle is False:
        self.sharpen = value
      else:
        self.sharpen = not self.sharpen
      if self.sharpen is True:
        self.filterimg = True
        self.selected_filters.append(ImageFilter.SHARPEN)
        loginfo("Sharpen On")
      else:
        #if len(self.selected_filters) <= 0: self.filterimg = False
        if ImageFilter.SHARPEN in self.selected_filters:
          self.selected_filters.remove(ImageFilter.SHARPEN)
          loginfo("Sharpen Off")
      self.display()


    @trace(3)
    def on_toggle_smooth(self,event):
        self.toggle_smooth()


    @trace(3)
    def toggle_smooth(self,toggle=True,value=True):
      if toggle is False:
        self.smooth = value
      else:
        self.smooth = not self.smooth
      if self.smooth is True:
        self.filterimg = True
        self.selected_filters.append(ImageFilter.SMOOTH)
        loginfo("Smooth On")
      else:
        #if len(self.selected_filters) <= 0: self.filterimg = False
        if ImageFilter.SMOOTH in self.selected_filters:
          self.selected_filters.remove(ImageFilter.SMOOTH)
          loginfo("Smooth Off")
      self.display()


    @trace(3)
    def on_toggle_smooth_more(self,event):
        self.toggle_smooth_more()


    @trace(3)
    def toggle_smooth_more(self,toggle=True,value=True):
      if toggle is False:
        self.smooth_more = value
      else:
        self.smooth_more = not self.smooth_more
      if self.smooth_more is True:
        self.filterimg = True
        self.selected_filters.append(ImageFilter.SMOOTH_MORE)
        loginfo("Smooth On")
      else:
        #if len(self.selected_filters) <= 0: self.filterimg = False
        if ImageFilter.SMOOTH_MORE in self.selected_filters:
          self.selected_filters.remove(ImageFilter.SMOOTH_MORE)
          loginfo("Smooth Off")
      self.display()


    @trace(3)
    def on_prev_slide(self,event):
      if self.image_mode is True:
        self.on_img_prev(event)
      else:
        self.on_file_prev(event)


    @trace(3)
    def prev_slide(self):
      if self.image_mode is True:
        self.img_prev()
      else:
        self.file_prev()


    @trace(3)
    def on_next_slide(self,event):
      if self.image_mode is True:
        self.on_img_next(event)
      else:
        self.on_file_next(event)


    @trace(3)
    def next_slide(self):
      # TODO: cancel timers and reset when moving a frame
      # TODO: lock on actions that can work on display between actions and the display method when running
      if self.image_mode is True:
        self.img_next()
      else:
        self.file_next()


    @trace(3)
    def on_img_prev(self,event):
      self.img_prev()


    @trace(3)
    def img_prev(self):
      self.prev_image()
      if self.timer is not None:
        self.stop()


    @trace(3)
    def prev_image(self,print_info=True):
      loginfo("Image:", self.iimages, "Length is", len(self.images), "Repeat is", self.repeat)
      if self.iimages > 0:
        self.iimages = self.iimages - 1
      elif self.repeat is True:
        self.iimages = len(self.images)
      else:
        loginfo("This is the first image in the sequence")
        self.statusinfolbl.config(text="Beginning of Sequence")
        self.stop()
        return False
      self.rawimg = self.images[self.iimages].copy()
      if print_info is True: self.print_image_info(self.rawimg,
                                                   show_file=False,
                                                   test_images=False,
                                                   check_format_modes=False,
                                                   check_palette=False)
      self.display()
      if self.toolbar is not None: self.savebtn['state'] = NORMAL


    @trace(3)
    def on_img_next(self,event):
      self.img_next()


    @trace(3)
    def img_next(self):
      self.next_image()
      if self.timer is not None:
        self.stop()


    @trace(3)
    def next_image(self,print_info=True):
      loginfo("Image:",self.iimages, "Length is", len(self.images), "Repeat is", self.repeat)
      if self.iimages < len(self.images) - 1:
        self.iimages = self.iimages + 1
      elif self.repeat is True:
        index = 0
      else:
        loginfo("This is the last image in the sequence")
        self.statusinfolbl.config(text="End of Sequence")
        self.stop()
        return False
      self.rawimg = self.images[self.iimages].copy()
      if print_info is True: self.print_image_info(self.rawimg,
                                                   show_file=False,
                                                   test_images=False,
                                                   check_format_modes=False,
                                                   check_palette=False)
      self.display()
      if self.toolbar is not None: self.savebtn['state'] = NORMAL


    @trace(3)
    def on_file_prev(self,event):
      if self.picture_frame is not None: self.picture_frame.focus_set()
      self.file_prev()


    @trace(3)
    def file_prev(self):
      self.previous_file()
      if self.timer is not None: self.stop()


    @trace(3)
    def previous_file(self):
      loginfo(self.seperator)
      loginfo("Previous Image File: isources =",self.isources,",repeat =",self.repeat,",len(sources) =",len(self.sources))
      if self.go_to_previous_file() is True:
        if len(self.sources) > self.isources:
          self.open_file(ntpath.join(self.root_directory,self.sources[self.isources]))
        else:
          logwarn("Index out of range",self.isources)


    @trace(3)
    def on_file_next(self,event):
      if self.picture_frame is not None: self.picture_frame.focus_set()
      self.file_next()


    @trace(3)
    def file_next(self):
      self.next_file()
      if self.timer is not None:
        self.stop()


    @trace(3)
    def next_file(self):
      loginfo(self.seperator)
      loginfo("Next Image File: isources =",self.isources,",repeat =",self.repeat,",len(sources) =",len(self.sources))
      loginfo("Sources Length is",len(self.sources), "Repeat is", self.repeat)
      if self.go_to_next_file() is True:
        if len(self.sources) > self.isources:
          self.open_file(ntpath.join(self.root_directory,self.sources[self.isources]))
        else:
          loginfo("Index out of range",self.isources)


    @trace(3)
    def on_file_random(self,event):
      if self.picture_frame is not None: self.picture_frame.focus_set()
      self.file_random()


    @trace(3)
    def file_random(self):
      loginfo(self.seperator)
      if self.next_random_file() is True:
        if len(self.sources) > self.isources:
          self.open_file(ntpath.join(self.root_directory,self.sources[self.isources]))
        else:
          loginfo("Index out of range",self.isources)
      if self.timer is not None:
        self.stop()


    @trace(3)
    def find_next_file(self,verbose=False): # not used, may need to pro
      """ Not Used Yet. This is just a find in case a presearch is needed to verify files exist. Returns True if matching file is found and the index of that file. """
      # TODO: look into using this in go_to_next_file
      # TODO: Update for video and other media files that may not be images
      count = 0
      found = False
      index = 0
      loginfo("Portrait is", self.portrait,"Landscape is", self.landscape, "High Quality is",self.highquality,"Low Quality is",self.lowquality)
      while index < len(self.sources) and found is not True:
        if verbose is True:
          loginfo("Scanning... Index:",index,"File:",self.sources[index])
        try:
          img = PIL.Image.open(ntpath.join(self.root_directory,self.sources[index]))
          if img.width < img.height: # portrait
            if self.highquality is True:
              if img.width > 800 and img.height > 1000:
                if self.portrait is True:
                  found = True
              else:
                if verbose is True:
                  logverb("Skipping (width={0},height={1}) -> {2}".format(img.width,img.height,self.sources[index]))
            elif self.lowquality is True:
              if img.width < 600 and img.height < 800:
                if self.portrait is True:
                  found = True
              else:
                if verbose is True:
                  logverb("Skipping (width={0},height={1}) -> {2}".format(img.width,img.height,self.sources[index]))
            else:
              if self.portrait is True:
                found = True
          elif img.width > img.height: # landscape
            if self.highquality is True:
              if img.width > 1000 and img.height > 800:
                if self.landscape is True:
                  found = True
              else:
                if verbose is True:
                  logverb("Skipping (width={0},height={1}) -> {2}".format(img.width,img.height,self.sources[index]))
            elif self.lowquality is True:
              if img.width < 800 and img.height < 600:
                if self.portrait is True:
                  found = True
              else:
                if verbose is True:
                  logverb("Skipping (width={0},height={1}) -> {2}".format(img.width,img.height,self.sources[index]))
            else:
              if self.landscape is True:
                found = True
          else: # it's a square; for now we'll side with it's both a portrait and a landscape
            if self.highquality is True:
              if img.width > 800 and img.height > 800:
                found = True
              else:
                if verbose is True:
                  logverb("Skipping (width={0},height={1}) -> {2}".format(img.width,img.height,self.sources[index]))
            elif self.lowquality is True:
              if img.width < 600 and img.height < 600:
                found = True
              else:
                if verbose is True:
                  logverb("Skipping (width={0},height={1}) -> {2}".format(img.width,img.height,self.sources[index]))
            else:
              found = True
          if found is True:
            if verbose is True:
              loginfo("Found Matching Image! width: {0}, height: {1} -> {2}",img.width,img.height,ntpath.join(self.root_directory,self.sources[index]))
          img.close()
        except Exception as e:
          exception(e)
        if found is not True:
          index = index + 1
          if index == len(self.sources):
            if verbose is True:
              loginfo("We've reached the end of the sequence")
            if self.repeat is True:
              index = 0
            else:
              self.stop()
              return False
          count = count + 1
          if count >= len(self.sources):
            if verbose is True:
              loginfo("Matching Image Not Found!")
            return False, self.isources # only check all entries once, return isources for safe fail. I.e. no change
      return True, index


    @trace(3)
    def go_to_previous_file(self):
      logverb("Previous Image: isources =",self.isources,",repeat =",self.repeat,",len(sources) =",len(self.sources))
      if self.random is True:
        if self.ihistory > 0:
          self.ihistory = self.ihistory - 1
        if self.ihistory >= 0:
          self.isources = self.history[self.ihistory]
        else:
          loginfo("At Start Of History, Index is", self.ihistory)
          return # no sense in reloading the file that is loaded
        loginfo("History Index is", self.ihistory)
        if len(self.sources) > self.isources:
          self.open_file(ntpath.join(self.root_directory,self.sources[self.isources]))
        else:
          logwarn("Index out of range",self.isources)
      #elif self.vidcap is not None:
      #  self.isources = index; found = True
      else:
        index = self.isources
        loginfo("Portrait is", self.portrait,"Landscape is", self.landscape, "High Quality is",self.highquality,"Low Quality is",self.lowquality)
        if index > 0:
          index = index - 1
        elif self.repeat is True:
          index = len(self.sources) - 1
        else:
          loginfo("This is the first file in the sequence")
          self.statusinfolbl.config(text="Beginning of Sequence")
          self.stop()
          return False
        self.statusinfolbl.config(text="")
        self.stauserrorlbl.config(text="")
        count = 0
        found = False
        while index > -1 and index < len(self.sources) and found is False:
          loginfo("Scanning... Index:",index,"File:",self.sources[index])
          try:
            self.file_name,self.file_ext = self.get_file_name_ext(self.sources[index])
            if self.file_ext is not None:
              if self.file_ext.lower() in self.supported_image_extensions:
                img = self.open_image(ntpath.join(self.root_directory,self.sources[index]),peek=True)
                if img is not None:
                  if img.width < img.height: # portrait
                    if self.highquality is True:
                      if img.width > 800 and img.height > 1000:
                        if self.portrait is True:
                          self.isources = index; found = True
                      else:
                        logverb("Skipping (width={0},height={1}) -> {2}".format(img.width,img.height,self.sources[index]))
                    elif self.lowquality is True:
                      if img.width < 600 and img.height < 800:
                        if self.portrait is True:
                          self.isources = index; found = True
                      else:
                        logverb("Skipping (width={0},height={1}) -> {2}".format(img.width,img.height,self.sources[index]))
                    else:
                      if self.portrait is True:
                        self.isources = index; found = True
                  elif img.width > img.height: # landscape
                    if self.highquality is True:
                      if img.width > 1000 and img.height > 800:
                        if self.landscape is True:
                          self.isources = index; found = True
                      else:
                        logverb("Skipping (width={0},height={1}) -> {2}".format(img.width,img.height,self.sources[index]))
                    elif self.lowquality is True:
                      if img.width < 800 and img.height < 600:
                        if self.landscape is True:
                          self.isources = index; found = True
                      else:
                        logverb("Skipping (width={0},height={1}) -> {2}".format(img.width,img.height,self.sources[index]))
                    else:
                      if self.landscape is True:
                        self.isources = index; found = True
                  else: # it's a square; for now we'll side with it's both a portrait and a landscape
                    if self.highquality is True:
                      if img.width > 800 and img.height > 800:
                        self.isources = index; found = True
                      else:
                        logverb("Skipping Low Quality Image:", self.sources[index])
                    elif self.lowquality is True:
                      if img.width < 600 and img.height < 600:
                        self.isources = index; found = True
                      else:
                        logverb("Skipping (width={0},height={1}) -> {2}".format(img.width,img.height,self.sources[index]))
                    else:
                      self.isources = index; found = True
                  if found is True:
                    loginfo("Found Matching Image! width: {0}, height: {1} -> {2}",img.width,img.height,ntpath.join(self.root_directory,self.sources[index]))
                  img.close()
                else:
                  if self.inspection_mode is True:
                    self.isources = index; found = True # open_file should hit same error not in peek mode
              elif self.file_ext.lower() in self.supported_video_extensions:
                if self.landscape is False or self.portrait is False:
                  loginfo("Skipping video in landscape and portrait modes for now ->",self.sources[index])
                  pass  #TODO: check for landscape, portrait, high and low quality video
                else:
                  self.isources = index; found = True
              else:
                logwarn("File",self.sources[index],"has unsupported format",self.file_ext)
            else:
              logwarn("File",self.sources[index],"has no extension so is an unknown format.")
          except Exception as e:
            exception(e)
          if found is not True:
            index = index - 1
            if index == -1:
              loginfo("We've reached the begining of the sequence")
              self.statusinfolbl.config(text="Begining of Sequence")
              if self.repeat is True:
                index = len(self.sources)-1
              else:
                self.stop()
                return False
            count = count + 1
            if count >= len(self.sources):
              loginfo("Image Not Found!")
              return False # only check all entries once
      return True


    @trace(3)
    def go_to_next_file(self):
      # TODO: sort by date?
      # TODO: qualify images by quality, needs to be above x width and x height
      # TODO: add try except on open in case file fails, must note this file as it may be noteworthy, update prev and rand counterparts as well
      logverb("Next Image: isources =",self.isources,",repeat =",self.repeat,",len(sources) =",len(self.sources))
      if self.random is True:
        # TODO: merge this with go_to_next_file maybe? I'm having second thoughts
        if self.ihistory < len(self.history)-1: # scrolling throuh self.history still
          self.ihistory = self.ihistory + 1
          self.isources = self.history[self.ihistory]
          loginfo("History Index is", self.ihistory)
          self.open_file(ntpath.join(self.root_directory,self.sources[self.isources]))
        else: # timeline is current so generate another image and move forward
          return self.next_random_file()
      #elif self.vidcap is not None:
      #  self.isources = index; found = True
      else:
        index = self.isources
        loginfo("Portrait is", self.portrait,"Landscape is", self.landscape, "High Quality is",self.highquality,"Low Quality is",self.lowquality)
        if index < len(self.sources) - 1:
          index = index + 1
        elif self.repeat is True:
          index = 0
        else:
          loginfo("This is the last file in the sequence")
          self.statusinfolbl.config(text="End of Sequence")
          self.stop()
          return False
        # get temp index, if no file is found our global index remains unchanged
        #index = self.isources
        self.statusinfolbl.config(text="")
        self.stauserrorlbl.config(text="")
        count = 0
        found = False
        while index < len(self.sources) and found is not True:
          loginfo("Scanning... Index:",index,"File:",self.sources[index])
          try:
            self.file_name,self.file_ext = self.get_file_name_ext(self.sources[index])
            if self.file_ext is not None:
              if self.file_ext.lower() in self.supported_image_extensions:
                img = self.open_image(ntpath.join(self.root_directory,self.sources[index]),peek=True)
                if img is not None:
                  if img.width < img.height: # portrait
                    if self.highquality is True:
                      if img.width > 800 and img.height > 1000:
                        if self.portrait is True:
                          self.isources = index; found = True
                      else:
                        logverb("Skipping (width={0},height={1}) -> {2}".format(img.width,img.height,self.sources[index]))
                    elif self.lowquality is True:
                      if img.width < 600 and img.height < 800:
                        if self.portrait is True:
                          self.isources = index; found = True
                      else:
                        logverb("Skipping (width={0},height={1}) -> {2}".format(img.width,img.height,self.sources[index]))
                    else:
                      if self.portrait is True:
                        self.isources = index; found = True
                  elif img.width > img.height: # landscape
                    if self.highquality is True:
                      if img.width > 1000 and img.height > 800:
                        if self.landscape is True:
                          self.isources = index; found = True
                      else:
                        logverb("Skipping (width={0},height={1}) -> {2}".format(img.width,img.height,self.sources[index]))
                    elif self.lowquality is True:
                      if img.width < 800 and img.height < 600:
                        if self.portrait is True:
                          self.isources = index; found = True
                      else:
                        logverb("Skipping (width={0},height={1}) -> {2}".format(img.width,img.height,self.sources[index]))
                    else:
                      if self.landscape is True: self.isources = index; found = True
                  else: # it's a square; for now we'll side with it's both a portrait and a landscape
                    if self.highquality is True:
                      if img.width > 800 and img.height > 800:
                        self.isources = index; found = True
                      else:
                        logverb("Skipping (width={0},height={1}) -> {2}".format(img.width,img.height,self.sources[index]))
                    elif self.lowquality is True:
                      if img.width < 600 and img.height < 600:
                        self.isources = index; found = True
                      else:
                        logverb("Skipping (width={0},height={1}) -> {2}".format(img.width,img.height,self.sources[index]))
                    else:
                      self.isources = index; found = True
                    if found is True:
                      loginfo("Found Matching Image! width: {0}, height: {1} -> {2}",img.width,img.height,ntpath.join(self.root_directory,self.sources[index]))
                    img.close()
                else:
                  if self.inspection_mode is True:
                    self.isources = index; found = True # open_file should hit same error not in peek mode
              elif self.file_ext.lower() in self.supported_video_extensions:
                if self.landscape is False or self.portrait is False:
                  loginfo("Skipping video in landscape and portrait modes for now ->",self.sources[index])
                  pass #TODO: check for landscape, portrait, high and low quality video
                else:
                  self.isources = index; found = True
              else:
                logwarn("File",self.sources[index],"has unsupported format",self.file_ext)
            else:
              logwarn("File",self.sources[index],"has no extension so is an unknown format.")
          except Exception as e:
            exception(e)
            self.log("Go To Next File Error\n"+str(e)+"\n"+ntpath.join(self.root_directory,self.sources[index]))
          if found is not True:
            index = index + 1
            if index == len(self.sources):
              loginfo("We've reached the end of the sequence")
              self.statusinfolbl.config(text="End of Sequence")
              if self.repeat is True:
                index = 0
              else:
                self.stop()
                return False
            count = count + 1
            if count >= len(self.sources):
              loginfo("Matching Image Not Found!")
              return False # only check all entries once
      return True


     # TODO: check random image history functionality, does it distiguish between shuffled and ordered? or is it just putting history from both and just using that on whichever one is loaded
    @trace(3)
    # FIXED: slide show with random selected is displaying images twice
    def next_random_file(self):
      # TODO: pri=0;sev=0; restart random slide show at the history pointer not the end
      # TODO: pri=0;sev=0; in random mode make home and end be the beginning and end of random slides in history
      # TODO: pri=0;sev=0; set a limit on number of slides generated with 0 being infinite. Once and Loop allow it to end or continue looping on the randomly generated set of slides if not infinite.
      # TODO: pri=0;sev=0; next and prev searches that get image dimensions and only displays wide or tall in random and sequential modes
      # TODO: reject random choices and retry if they have been already displayed in the last X number of tries
      # TODO: <<NEXT>> Landscape and Portrait
      loginfo("Portrait is", self.portrait,"Landscape is", self.landscape, "High Quality is",self.highquality,"Low Quality is",self.lowquality)
      self.statusinfolbl.config(text="")
      self.stauserrorlbl.config(text="")
      if self.portrait is True and self.landscape is False:
        loginfo("*** LOOKING FOR PORTRAITS")
        portraits = []
        print("Gathering up all Portraits to randomly sample, this may take a moment ...")
        for filename in self.sources:
          try:
            self.file_name,self.file_ext = self.get_file_name_ext(filename)
            if self.file_ext is not None:
              if self.file_ext.lower() in self.supported_image_extensions:
                img = self.open_image(ntpath.join(self.root_directory,filename),peek=True)
                if img is not None:
                  if img.width <= img.height: # we also accept squares
                    if self.highquality is True:
                      if img.width > 800 and img.height > 1000:
                        logverb("Appending HQ (width={0},height={1}) -> {2}".format(img.width,img.height,filename))
                        portraits.append(filename)
                      else:
                        logverb("Skipping HQ (width={0},height={1}) -> {2}".format(img.width,img.height,filename))
                    elif self.lowquality is True:
                      if img.width < 600 and img.height < 800:
                        logverb("Appending HQ (width={0},height={1}) -> {2}".format(img.width,img.height,filename))
                        portraits.append(filename)
                      else:
                        logverb("Skipping LQ (width={0},height={1}) -> {2}".format(img.width,img.height,filename))
                    else:
                      logverb("Appending HQ (width={0},height={1}) -> {2}".format(img.width,img.height,filename))
                      portraits.append(filename)
                  img.close()
                else:
                  if self.inspection_mode is True:
                    portraits.append(filename) # open_file should hit same error not in peek mode
              elif self.file_ext.lower() in self.supported_video_extensions:
                loginfo("Skipping video in random portrait mode for now ->",self.sources[index])
                pass # TODO: check for portrait video
              else:
                logwarn("File",filename,"has unsupported format",ext)
            else:
              logwarn("File",filename,"has no extension so is an unknown format.")
          except Exception as e:
            exception(e)
            self.log("Next Random File Error\n"+str(e)+"\n"+ntpath.join(self.root_directory,filepathname))
        if len(portraits) > 0:
          self.isources = self.sources.index(random.choice(portraits))
        else:
          # there are no portraits to show
          # TODO: disable application in this instance and re-enable when this conditon is lifted
          logwarn("There are no Portraits available to display!")
          self.statusinfolbl.config(text="No Portraits Found")
          return False
      elif self.landscape is True and self.portrait is False:
        loginfo("*** LOOKING FOR LANDSCAPES")
        landscapes = []
        print("Gathering up all Landscapes to randomly sample, this may take a moment ...")
        for filename in self.sources:
          try:
            self.file_name,self.file_ext = self.get_file_name_ext(filename)
            if self.file_ext is not None:
              if self.file_ext.lower() in self.supported_image_extensions:
                img = self.open_image(ntpath.join(self.root_directory,filename),peek=True)
                if img is not None:
                  if img.width >= img.height: # we also accept squares
                    if self.highquality is True:
                      if img.width > 1000 and img.height > 800:
                        logverb("Collecting HQ (width={0},height={1}) -> {2}".format(img.width,img.height,filename))
                        landscapes.append(filename)
                      else:
                        logverb("Skipping HQ (width={0},height={1}) -> {2}".format(img.width,img.height,filename))
                    elif self.lowquality is True:
                        if img.width < 800 and img.height < 600:
                          logverb("Collecting HQ (width={0},height={1}) -> {2}".format(img.width,img.height,filename))
                          landscapes.append(filename)
                        else:
                          logverb("Skipping LQ (width={0},height={1}) -> {2}".format(img.width,img.height,filename))
                    else:
                      logverb("Collecting HQ (width={0},height={1}) -> {2}".format(img.width,img.height,filename))
                      landscapes.append(filename)
                  img.close()
                else:
                  if self.inspection_mode is True:
                    landscapes.append(filename) # open_file should hit same error not in peek mode
              elif self.file_ext.lower() in self.supported_video_extensions:
                loginfo("Skipping video in random landscape mode for now ->",self.sources[index])
                pass #TODO: check for landscape video
              else:
                logwarn("File",self.sources[index],"has unsupported format",self.file_ext)
            else:
              logwarn("File",filename,"has no extension so is an unknown format.")
          except Exception as e:
            exception(e)
            self.log("Next Random File Error\n"+str(e)+"\n"+ntpath.join(self.root_directory,filepathname))
        if len(landscapes) > 0:
          self.isources = self.sources.index(random.choice(landscapes))
        else:
          # there are no landscapes to show
          # TODO: disable application in this instance and re-enable when this conditon is lifted
          logwarn("There are no Landscapes available to display!")
          self.statusinfolbl.config(text="No Landscapes Found!")
          return False
      else: # all files
        print("Gathering up all Qaulifying files to randomly sample, this may take a moment ...")
        if self.highquality is False and self.lowquality is False:
          self.isources = random.randint(0,len(self.sources)-1)
        else:
          images = []
          for filename in self.sources:
            try:
              self.file_name,self.file_ext = self.get_file_name_ext(filename)
              if self.file_ext is not None:
                if self.file_ext.lower() in self.supported_image_extensions:
                  img = self.open_image(ntpath.join(self.root_directory,filename),peek=True)
                  if img is not None:
                    if img.width < img.height: # portrait
                      if self.highquality is True:
                        if img.width > 800 and img.height > 1000:
                          logverb("Collecting HQ (width={0},height={1}) -> {2}".format(img.width,img.height,filename))
                          images.append(filename)
                        else:
                          logverb("Skipping HQ (width={0},height={1}) -> {2}".format(img.width,img.height,filename))
                      elif self.lowquality is True:
                        if img.width < 600 and img.height < 800:
                          logverb("Collecting LQ (width={0},height={1}) -> {2}".format(img.width,img.height,filename))
                          images.append(filename)
                        else:
                          logverb("Skipping LQ (width={0},height={1}) -> {2}".format(img.width,img.height,filename))
                      else:
                        images.append(filename)
                    elif img.width > img.height: # landscape
                      if self.highquality is True:
                        if img.width > 1000 and img.height > 800:
                          logverb("Collecting HQ (width={0},height={1}) -> {2}".format(img.width,img.height,filename))
                          images.append(filename)
                        else:
                          logverb("Skipping HQ (width={0},height={1}) -> {2}".format(img.width,img.height,filename))
                      elif self.lowquality is True:
                          if img.width < 800 and img.height < 600:
                            logverb("Collecting LQ (width={0},height={1}) -> {2}".format(img.width,img.height,filename))
                            images.append(filename)
                          else:
                            logverb("Skipping LQ (width={0},height={1}) -> {2}".format(img.width,img.height,filename))
                      else:
                        logverb("Collecting (width={0},height={1}) -> {2}".format(img.width,img.height,filename))
                        images.append(filename)
                    else: # square
                      if self.highquality is True:
                        if img.width > 800 and img.height > 800:
                          logverb("Collecting HQ (width={0},height={1}) -> {2}".format(img.width,img.height,filename))
                          images.append(filename)
                        else:
                          logverb("Skipping HQ (width={0},height={1}) -> {2}".format(img.width,img.height,filename))
                      elif self.lowquality is True:
                          if img.width < 600 and img.height < 600:
                            logverb("Collecting LQ (width={0},height={1}) -> {2}".format(img.width,img.height,filename))
                            images.append(filename)
                          else:
                            logverb("Skipping LQ (width={0},height={1}) -> {2}".format(img.width,img.height,filename))
                      else:
                        logverb("Collecting (width={0},height={1}) -> {2}".format(img.width,img.height,filename))
                        images.append(filename)
                    img.close()
                  else:
                    if self.inspection_mode is True:
                      images.append(filename) # open_file should hit same error not in peek mode
                elif self.file_ext.lower() in self.supported_video_extensions:
                  logverb("Collecting (width=\{0\},height=\{1\}) -> {2}".format(img.width,img.height,filename))
                  images.append(filename)
                else:
                  logwarn("File",self.sources[index],"has unsupported format",self.file_ext)
              else:
                logwarn("File",filename,"has no extension so is an unknown format.")
            except Exception as e:
              exception(e)
              self.log("Next Random File Error\n"+str(e)+"\n"+ntpath.join(self.root_directory,filepathname))
          if len(images) > 0:
            self.isources = self.sources.index(random.choice(images))
            loginfo("Images",images)
          else:
            # there are no images to show
            # TODO: disable application in this instance and re-enable when this conditon is lifted
            logwarn("There are no qualifying images available to display!")
            self.statusinfolbl.config(text="No Qualifying Images Found!")
            return False
      # TODO: should we still open the file after an exception? maybe this should go above the execption in the try code block
      self.history.append(self.isources)
      if self.debug is True: loginfo("History",self.history)
      self.ihistory = len(self.history)-1
      loginfo("Next File is", self.sources[self.isources])
      loginfo("Random Image: isources =",self.isources,",len =",len(self.sources))
      loginfo("History Index is", self.ihistory)
      return True


    @trace(1)
    def on_play_pause(self,event):
      self.play_pause()


    @trace(1)
    def play_pause(self):
      loginfo("Play")
      if self.is_GIF_file is True:
        if self.playing is False:
          loginfo("Begin GIF Animation ...")
          self.playing = True
          time_length = 30.0
          fps=25
          frame_seq = 749
          frame_no = (frame_seq /(time_length*fps))
          self.playbtn.config(text='||')
          self.end_of_stream = False

          self.advance_gif_frames()
        else:
          loginfo("Pause")
          self.playing = False
          self.playbtn.config(text='>')
      elif self.vidcap is not None:
        if self.playing is False:
          self.playing = True
          loginfo("Begin Video Playback ...")
          #Set frame_no in range 0.0-1.0
          #In this example we have a video of 30 seconds having 25 frames per seconds, thus we have 750 frames.
          #The examined frame must get a value from 0 to 749.
          #For more info about the video flags see here: https://stackoverflow.com/questions/11420748/setting-camera-parameters-in-opencv-python
          #Here we select the last frame as frame sequence=749. In case you want to select other frame change value 749.
          #BE CAREFUL! Each video has different time length and frame rate.
          #So make sure that you have the right parameters for the right video!
          # TODO: integrate these variables into the class
          time_length = 30.0
          fps=25
          frame_seq = 749
          frame_no = (frame_seq /(time_length*fps))
          self.playbtn.config(text='||')
          self.end_of_stream = False
          self.advance_cv_frames()
        else:
          loginfo("Pause")
          self.playing = False
          self.playbtn.config(text='>')


    @trace(3)
    def advance_gif_frames(self):
      if self.is_GIF_file is True and self.playing is True and self.rawimg.n_frames:
        self.frame = (self.frame + 1)
        if self.frame >= self.rawimg.n_frames:
          if self.repeat is True:
            self.frame = 0
          else:
            self.play_pause()
            return
        loginfo("GIF Frame", self.frame)
        try:
          self.rawimg.seek(self.frame)
          self.display()
          self.framecntr.set(str(self.frame+1) + "/" + str(self.rawimg.n_frames))
        except Exception as e:
          exception(e)
          self.playing is False
        if self.is_GIF_file is True and self.playing is True:
          self.canvas.after(66, self.advance_gif_frames)


    @trace(3)
    def advance_cv_frames(self):
      # https://stackoverflow.com/questions/37799847/python-playing-a-video-with-audio-with-opencv
      # https://stackoverflow.com/questions/65909503/how-can-i-play-video-in-opencv-with-audio-the-same-time
      if self.playing is True and self.vidcap is not None:
        self.process_cv_frame()
        # TODO: replace with more advance frame looping using time delta like a game and setting for time - delta to compensate for processing time
        if self.playing is True and self.vidcap is not None:
          self.canvas.after(33, self.advance_cv_frames)


    @trace(3)
    def process_cv_frame(self,print_image=False):
      if self.vidcap is not None:
        loginfo("CV Frame",self.vidcap.get(self.eCap.CV_CAP_PROP_POS_FRAMES))
        ret_val, frame = self.vidcap.read()
        # https://stackoverflow.com/questions/18954889/how-to-process-images-of-a-video-frame-by-frame-in-video-streaming-using-openc
        # while True:
          # flag, frame = self.vidcap.read()
          # if flag:
              # # The frame is ready and already captured
              # cv2.imshow('video', frame)
              # pos_frame = self.vidcap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
              # print str(pos_frame)+" frames"
          # else:
              # # The next frame is not ready, so we try to read it again
              # self.vidcap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, pos_frame-1)
              # print "frame is not ready"
              # # It is better to wait for a while for the next frame to be ready
              # cv2.waitKey(1000)

          # if cv2.waitKey(10) == 27:
              # break
          # if self.vidcap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES) == self.vidcap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT):
              # # If the number of captured frames is equal to the total number of frames,
              # # we stop
              # break
        if ret_val is True and frame is not None:
          # reduce to just the few items that really help eventually, for now I want to observe all for any changes
          self.print_video_info(self.vidcap, changes_only=not self.debug) # so far just 'Current Timestamp' and 'Next Frame' changes
          #if self.mirror: frame = cv2.flip(frame, 1)
          # https://docs.opencv.org/master/d8/d01/group__imgproc__color__conversions.html
          # https://www.geeksforgeeks.org/python-opencv-cv2-cvtcolor-method/
          cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
          if print_image is True:
            loginfo("Image:: Length:",len(cv2image),"->:",cv2image)
          # https://www.geeksforgeeks.org/python-process-images-of-a-video-using-opencv/
          # adaptive thresholding to use different threshold
          # values on different regions of the frame.
          #cv2image = cv2.adaptiveThreshold(cv2image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)

          self.rawimg = Image.fromarray(cv2image)
          self.display()
          #if cv2.waitKey(300) == 27: self.stop()
        else:
          if self.end_of_stream is False: # print only once as I may leave running after it ends so chaning to other videos is continuous
            logverb("No More CVFrames to Process")
            if self.debug is True: loginfo("Return",ret_val, ", Frame is",frame)
            if self.repeat is True:
              self.vidcap.set(2,0)
              cv2.waitKey(1000)
            else:
              self.play_pause()
              self.end_of_stream = True
      else:
        logwarn("Nothing to Process")


    @trace(3)
    def seek_home(self):
      loginfo("Seek Home")
      if self.is_GIF_file is True:
        self.frame = 0
        loginfo("Seeking Frame",self.frame)
        self.rawimg.seek(self.frame)
        self.display()
        self.framecntr.set(str(self.frame+1) + "/" + str(self.rawimg.n_frames))
      elif self.vidcap is not None:
        loginfo("Seek Position", 0)
        self.vidcap.set(2,0)
        cv2.waitKey(1000)
        self.process_cv_frame()
      else:
        loginfo("is_GIF_file",self.is_GIF_file,"vidcap",self.vidcap)


    @trace(3)
    def seek_end(self):
      loginfo("Seek End")
      if self.is_GIF_file is True:
        self.frame = self.rawimg.n_frames - 1
        loginfo("Seeking Frame",self.frame)
        self.rawimg.seek(self.frame) # EOFError
        self.display()
        self.framecntr.set(str(self.frame+1) + "/" + str(self.rawimg.n_frames))
      elif self.vidcap is not None:
        seek_pos = int(self.vidcap.get(self.eCap.CV_CAP_PROP_FRAME_COUNT)-1)
        loginfo("Seek Position", seek_pos)
        self.vidcap.set(2,seek_pos)
        cv2.waitKey(1000)
        self.process_cv_frame()
      else:
        loginfo("is_GIF_file",self.is_GIF_file,"vidcap",self.vidcap)


    @trace(3)
    def frame_seek_prev(self):
      # DONE: fix seek so it actually works, its displaying now for all GIF's it just needs to functional
      # https://www.geeksforgeeks.org/python-pil-image-seek-method/
      # https://www.geeksforgeeks.org/python-pil-image-tell/
      # https://pillow.readthedocs.io/en/5.2.x/reference/plugins.html#PIL.GifImagePlugin.GifImageFile.n_frames
      if self.debug is True: loginfo("Call Display frame_seek_prev")
      try:
        if self.is_GIF_file is True:
          #self.filtimg.seek(self.filtimg.tell()-1)
          #self.framecntr.set(str(self.rawimg.tell()) + "/" +  str(self.rawimg.n_frames))
          self.frame = self.frame - 1
          if self.frame < 0:
            self.frame = 0
          loginfo("Seeking Frame",self.frame)
          self.rawimg.seek(self.frame)
          self.display()
          self.framecntr.set(str(self.frame+1) + "/" + str(self.rawimg.n_frames))
        elif self.vidcap is not None:
          seek_pos = self.eCap.CV_CAP_PROP_POS_FRAMES-2
          loginfo("Seek Position", seek_pos)
          self.vidcap.set(2,seek_pos)
          cv2.waitKey(1000)
          self.process_cv_frame()
        else:
          loginfo("is_GIF_file",self.is_GIF_file,"vidcap",self.vidcap)
      except:
        pass
      self.display(resize=False)


    @trace(3)
    def frame_seek_next(self):
      if self.debug is True: loginfo("Call Display frame_seek_next")
      try:
        if self.is_GIF_file is True:
          #self.filtimg.seek(self.filtimg.tell()+1)
          #self.framecntr.set(str(self.rawimg.tell()) + "/" +  str(self.rawimg.n_frames))
          self.frame = self.frame + 1
          try:
            loginfo("Seeking Frame",self.frame)
            self.rawimg.seek(self.frame)
            self.display()
            self.framecntr.set(str(self.frame+1) + "/" + str(self.rawimg.n_frames))
          except:
            self.frame=self.frame-1
        elif self.vidcap is not None:
          seek_pos = int(self.vidcap.get(self.eCap.CV_CAP_PROP_POS_FRAMES)-1)
          loginfo("Seek Position", seek_pos)
          self.vidcap.set(2,seek_pos)
          cv2.waitKey(1000)
          self.process_cv_frame()
        else:
          loginfo("is_GIF_file",self.is_GIF_file,"vidcap",self.vidcap)
      except:
        pass
      self.display(resize=False)


    @trace(3)
    def stop_slideshow(self):
      # DONE: pri=0;sev=0; have the timer reset when the timer increment is changed to reflect the change immediatly instead of after the interval already in progress finishes
      if self.timer is not None:
        loginfo("Stopping Slide Show")
        self.timer.cancel()
        self.timer = None
        self.showbtn.config(text="Start")


    @trace(3)
    def on_stop(self,event):
      self.stop()


    @trace(3)
    def stop(self):
      self.stop_slideshow()


    @trace(3)
    def on_start(self,event):
      self.start()


    @trace(3)
    def start(self):
      self.start_slideshow()


    @trace(3)
    def on_repeat(self,event):
      self.toggle_repeat()


    @trace(3)
    def toggle_repeat(self,toggle=True,value=True):
      if toggle is False:
        self.repeat = value
      else:
        self.repeat = not self.repeat
      loginfo("Toggle Repeat to",self.repeat)
      if self.repeat is True:
        self.repeatbtn.config(text="Loop")
      else:
        self.repeatbtn.config(text="Once")


    @trace(3)
    def on_toggle_random(self,event):
        self.toggle_random()


    @trace(3)
    def toggle_random(self,toggle=True,value=True):
      if toggle is False:
        self.random = value
      else:
        self.random = not self.random
      loginfo("Toggle Random to",self.random)
      if self.random is True:
        self.randombtn.config(text="Rand")
        if len(self.history) <= 0:
          self.ihistory = self.isources
          self.history.append(self.isources)
      else:
        self.randombtn.config(text="A-Z")


    @trace(3)
    def on_toggle_shuffle(self,event):
        self.toggle_shuffle()


    # TODO: test shuffle. E.g. i can't visually tell if it is at the correct index when switching in an out of shuffle. It could be going to anywhere in the shuffled slide deck when switching back. It is supposed to remember where it was and resume at that point.
    @trace(3)
    def toggle_shuffle(self,toggle=True,value=True):
      if toggle is False:
        self.shuffle = value
      else:
        self.shuffle = not self.shuffle
      loginfo("Toggle Shuffle to",self.shuffle)
      if self.shuffle is True:
        loginfo("Shuffled")
        self.shufflebtn.config(text="Order")
        self.isources = self.ishuffled_sources # back to saved state (where it left off)
        self.sources = self.shuffled_sources
        if len(self.ordered_sources) > 0:
          self.open_file(ntpath.join(self.root_directory,self.sources[self.isources]))
      else:
        loginfo("Ordered")
        self.shufflebtn.config(text="Shuffle")
        self.ishuffled_sources = self.isources # save state
        try:
          # find same file in the ordered sources and start from there, this should be the file currently displayed in shuffle
          self.isources = self.ordered_sources.index(self.sources[self.isources])
        except ValueError as e:
          logerror("Source not found! ->", self.sources[self.isources])
          self.isources = self.ishuffled_sources # I'm not sure of the state of self.isources after failure so setting again here
        self.sources = self.ordered_sources
        if len(self.ordered_sources) > 0:
          self.open_file(ntpath.join(self.root_directory,self.sources[self.isources]))


    @trace(3)
    def on_toggle_portrait(self,event):
      self.toggle_portrait()


    @trace(3)
    def toggle_portrait(self,toggle=True,value=True):
      if toggle is False:
        if self.portrait == value: return # so we can set from landscape without recursion
        self.portrait = value
      else:
        self.portrait = not self.portrait
      loginfo("Toggle Portrait to",self.portrait, "Landscape is", self.landscape)
      if self.portrait is True:
        self.portraitbtn.config(text=" [*] ")
        #if self.landscape is True:
        #  self.toggle_landscape(toggle=False,value=False)
      else:
        self.portraitbtn.config(text=" [x] ")
        if self.landscape is False:
          self.toggle_landscape(toggle=False,value=True)


    @trace(3)
    def on_toggle_landscape(self,event):
        self.toggle_landscape()


    @trace(3)
    def toggle_landscape(self,toggle=True,value=True):
      if toggle is False:
        if self.landscape == value: return # avoid recursion
        self.landscape = value
      else:
        self.landscape = not self.landscape
      loginfo("Toggle Lanscape to",self.landscape, "Portrait is", self.portrait)
      if self.landscape is True:
        self.landscapebtn.config(text="[  *  ]")
        #if self.portrait is True:
        #  self.toggle_portrait(toggle=False,value=False)
      else:
        self.landscapebtn.config(text="[  x  ]")
        if self.portrait is False:
          self.toggle_portrait(toggle=False,value=True)


    @trace(3)
    def on_toggle_lowquality(self,event):
        self.toggle_lowquality()


    @trace(3)
    def toggle_lowquality(self,toggle=True,value=True):
      if toggle is False:
        if self.lowquality == value: return # avoid recursion
        self.lowquality = value
      else:
        self.lowquality = not self.lowquality
      loginfo("Toggle Low Quality to",self.lowquality,"High Quality is",self.highquality)
      if self.lowquality is True:
        self.lowqualitybtn.config(text="~")
        if self.highquality is True:
          self.toggle_highquality(toggle=False,value=False)
      else:
        self.lowqualitybtn.config(text="@")


    @trace(3)
    def on_toggle_highquality(self,event):
        self.toggle_highquality()


    @trace(3)
    def toggle_highquality(self,toggle=True,value=True):
      if toggle is False:
        if self.highquality == value: return # avoid recursion
        self.highquality = value
      else:
        self.highquality = not self.highquality
      loginfo("Toggle High Quality to",self.highquality,"Low Quality is",self.lowquality)
      if self.highquality is True:
        self.highqualitybtn.config(text="$")
        if self.lowquality is True:
          self.toggle_lowquality(toggle=False,value=False)
      else:
        self.highqualitybtn.config(text="*")


    @trace(3)
    def on_size(self, event=None):
      loginfo("WM_SIZE event",event)
      pause()


    @trace(3)
    def on_closing(self, event=None):
      if self.desktop_mode is True:
        self.toggle_desktop_mode(toggle=False,value=False)
      if len(self.images) > 0:
        for image in self.images:
          image.close()
      if self.timer is not None: self.timer.cancel()
      self.close_images()
      self.master.destroy() # to cancel close don't call this


    @trace(3)
    def on_motion(self,event):
      """ Display mouse move events """
      cx=event.x_root-self.master.winfo_x()
      cy=event.y_root-self.master.winfo_y()
      loginfo("X",cx,"Y",cy)


    @trace(3)
    def on_click(self,event):
      """ Handle mouse single click events """
      logverb(self.seperator)
      cx=event.x_root-self.master.winfo_x() # TODO: this is wrong, see winfo.py
      cy=event.y_root-self.master.winfo_y() # TODO: this is wrong, see winfo.py
      logverb("A: Mouse  : X",cx,", Y",cy)
      #loginfo("Event  : X", event.x_root, ", Y", event.y_root)
      # https://stackoverflow.com/questions/30257574/how-to-get-the-widgets-current-x-and-y-coordinates
      logverb("B: WInfo_Root: X", self.master.winfo_rootx(), ", Y", self.master.winfo_rooty())
      logverb("WInfo  : X", self.master.winfo_x(), ", Y", self.master.winfo_y())
      logverb("Toolbar: X", self.toolbar.winfo_x(),
                      ", Y", self.toolbar.winfo_y(),
                      ", Width",self.toolbar.winfo_width(),
                      ", Height",self.toolbar.winfo_height())
      if self.picture_frame is not None:
        logverb("Picture: X", self.picture_frame.winfo_x(),
                        ", Y", self.picture_frame.winfo_y(),
                        ", Width",self.picture_frame.winfo_width(),
                        ", Height",self.picture_frame.winfo_height())
      if self.tb_cmdtool is not None:
        logverb("Console: X", self.tb_cmdtool.winfo_x(),
                        ", Y", self.tb_cmdtool.winfo_y(),
                        ", Width",self.tb_cmdtool.winfo_width(),
                        ", Height",self.tb_cmdtool.winfo_height())
      if cx > self.master.winfo_rootx() and cy > self.master.winfo_rooty():
        loginfo("*** Set Focus to the Picture Window! ***")
        self.picture_frame.focus_set()
      else:
        logverb("Dammit!")
      logverb(self.seperator)


    @trace(3)
    def set_window_color(self,color):
      self.master.config(bg=color)
      self.picture_frame.config(bg=color)
      self.canvas.config(bg=color)
      icolor = self.getIfromPoundStr(color)
      loginfo("icolor",icolor)

      if icolor > 0x444444 and icolor < 0xdddddd:
        itextcolor = 0x000000
      else:
        itextcolor = ~icolor
      textcolor = self.getPoundStrFromI(itextcolor)
      loginfo("icolor",icolor,", itextcolor",itextcolor,", textcolor",textcolor)
      self.leftbtn.config(background=color,foreground=textcolor)
      self.rightbtn.config(background=color,foreground=textcolor)


    @trace(3)
    def img_replace_color(self,img):
      # https://medium.com/analytics-vidhya/some-interesting-tricks-in-python-pillow-8fe5acce6084
      datas = img.getdata()
      new_image_data = []
      for item in datas:
        # change all white (also shades of whites) pixels to yellow
        if item[0] in list(range(190, 256)):
          new_image_data.append((255, 204, 100))
        else:
          new_image_data.append(item)# update image data
      img.putdata(new_image_data)


    @trace(3)
    def get_exif_from_file(self,image_file_path):
      # # https://www.blog.pythonlibrary.org/2021/01/13/getting-gps-exif-data-with-python/
      image = Image.open(image_file_path)
      exif = get_exif(image)
      image.close()
      return exif


    @trace(3)
    def get_exif(self,image):
      exif = {}
      info = image.getexif()
      for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        exif[decoded] = value
      return exif


    # https://stackoverflow.com/questions/765736/how-to-use-pil-to-make-all-white-pixels-transparent
    # https://pythonprogramming.altervista.org/pil-create-a-transparent-image/
    @trace(3)
    def white_to_transparency(self,img):
      x = np.asarray(img.convert('RGBA')).copy()
      x[:, :, 3] = (255 * (x[:, :, :3] != 255).any(axis=2)).astype(np.uint8)
      return Image.fromarray(x)


    @trace(3)
    def white_to_transparency_gradient(self,img):
      x = np.asarray(img.convert('RGBA')).copy()
      x[:, :, 3] = (255 - x[:, :, :3].mean(axis=2)).astype(np.uint8)
      return Image.fromarray(x)


    @trace(3)
    # picked this image manipulation up from some samples, just going to have to try it to find out what it does
    def againreally(self,img):
      img = img.convert("RGBA")
      datas = img.getdata()
      newData = []
      for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
          newData.append((255, 255, 255, 0))
        else:
          newData.append(item)
      img.putdata(newData)
      return img


    @trace(3)
    # picked this image manipulation up from some samples, just going to have to try it to find out what it does
    def notsure(self,img):
      img = img.convert("RGBA")
      imgnp = np.array(img)
      white = np.sum(imgnp[:,:,:3], axis=2)
      white_mask = np.where(white == 255*3, 1, 0)
      alpha = np.where(white_mask, 0, imgnp[:,:,-1])
      imgnp[:,:,-1] = alpha
      img = Image.fromarray(np.uint8(imgnp))


    @trace(3)
    # picked this image manipulation up from some samples, just going to have to try it to find out what it does
    def dontknow(self,img):
      img = img.convert("RGBA")
      pixdata = img.load()
      width, height = img.size
      for y in range(height):
        for x in range(width):
          if pixdata[x, y] == (255, 255, 255, 255):
            pixdata[x, y] = (255, 255, 255, 0)


    @trace(3)
    def getPoundStrFromI(self,icolor):
      #'{:X}'.format(icolor & (2**32-1))
      #istr = hex(icolor & (2**32-1)) # 32-bit
      #istr = hex(icolor & (2**64-1)) # 64-bit
      #istr = hex(icolor & (2**24-1))
      istr = '{:06X}'.format(icolor & (2**24-1))
      loginfo("istr",istr)
      return '#{}'.format(istr)


    @trace(3)
    def getIfromPoundStr(self,RGBPoundStr):
      # https://stackoverflow.com/questions/51350872/python-from-color-name-to-rgb
      #if RGBPountStr[0] != '#':
      #  RGBPoundStr = colors.to_rgba(RGBPoundStr)
      # orange_rgb = colors.hex2color(colors.cnames['orange'])
      istr = RGBPoundStr.strip("'#'")
      loginfo("istr = ",istr)
      i = int(istr,16)
      loginfo("i = ",i)
      return i


    @trace(3)
    def getRGBfromPoundStr(self,RGBPoundStr):
      return getRGBfromI(self.getIfromPoundStr(RGBPoundStr))


    @trace(3)
    def getRGBfromI(self,RGBint):
      blue =  RGBint & 255
      green = (RGBint >> 8) & 255
      red =   (RGBint >> 16) & 255
      return red, green, blue


    @trace(3)
    def getIfromRGB(self,rgb):
      red = rgb[0]
      green = rgb[1]
      blue = rgb[2]
      loginfo(red, green, blue)
      RGBint = (red<<16) + (green<<8) + blue
      return RGBint


    @trace(1)
    def __del__(self):
      self.close_video_file()


    custom_filters = {
                 'blackvelvetpainting':[ImageFilter.SMOOTH_MORE,
                                       ImageFilter.SMOOTH,
                                       ImageFilter.DETAIL,
                                       ImageFilter.SMOOTH_MORE,
                                       ImageFilter.EDGE_ENHANCE,
                                       ImageFilter.FIND_EDGES],
                'blackvelvetpainting2':[ImageFilter.SMOOTH,
                                       ImageFilter.SMOOTH_MORE,
                                       ImageFilter.SMOOTH,
                                       ImageFilter.DETAIL,
                                       ImageFilter.SMOOTH_MORE,
                                       ImageFilter.EDGE_ENHANCE,
                                       ImageFilter.FIND_EDGES],
                'blackvelvetpainting3':[ImageFilter.SMOOTH_MORE, # worst one of the bunch
                                       ImageFilter.FIND_EDGES,
                                       ImageFilter.SMOOTH_MORE],
                'blackvelvetpainting4':[ImageFilter.SMOOTH_MORE,
                                       ImageFilter.FIND_EDGES],
                'blackvelvetpainting5':[ImageFilter.EDGE_ENHANCE_MORE,
                                       ImageFilter.SMOOTH_MORE,
                                       ImageFilter.FIND_EDGES],
                 'oldfashioneddrawing':[ImageFilter.SMOOTH_MORE,
                                       ImageFilter.SHARPEN,
                                       ImageFilter.EDGE_ENHANCE,
                                       ImageFilter.DETAIL,
                                       ImageFilter.CONTOUR,
                                       ImageFilter.SHARPEN],
                'oldfashioneddrawing2':[ImageFilter.SMOOTH,
                                       ImageFilter.EDGE_ENHANCE,
                                       ImageFilter.SMOOTH_MORE,
                                       ImageFilter.SHARPEN,
                                       ImageFilter.CONTOUR,
                                       ImageFilter.CONTOUR],
                             'enhance':[ImageFilter.EDGE_ENHANCE,
                                       ImageFilter.SMOOTH],
                              'scroll':[ImageFilter.DETAIL,
                                       ImageFilter.SHARPEN,
                                       ImageFilter.SMOOTH,
                                       ImageFilter.EDGE_ENHANCE,
                                       ImageFilter.EDGE_ENHANCE,
                                       ImageFilter.CONTOUR,
                                       ImageFilter.SHARPEN,
                                       ImageFilter.EDGE_ENHANCE,
                                       ImageFilter.EDGE_ENHANCE,
                                       ImageFilter.EDGE_ENHANCE_MORE],
                          'embroidery':[ImageFilter.FIND_EDGES,
                                       ImageFilter.EDGE_ENHANCE],
                          'watercolor':[ImageFilter.SMOOTH,
                                       ImageFilter.EDGE_ENHANCE_MORE,
                                       ImageFilter.EDGE_ENHANCE_MORE,
                                       ImageFilter.SMOOTH_MORE,
                                       ImageFilter.SHARPEN,
                                       ImageFilter.SHARPEN,
                                       ImageFilter.EDGE_ENHANCE],
                         'watercolor2':[ImageFilter.EDGE_ENHANCE_MORE,
                                       ImageFilter.DETAIL,
                                       ImageFilter.SHARPEN,
                                       ImageFilter.EDGE_ENHANCE_MORE,
                                       ImageFilter.FIND_EDGES,
                                       ImageFilter.DETAIL,
                                       ImageFilter.SMOOTH_MORE],
                       'brightnfluffy':[ImageFilter.EDGE_ENHANCE,
                                       ImageFilter.DETAIL,
                                       ImageFilter.SMOOTH_MORE,
                                       ImageFilter.EDGE_ENHANCE,
                                       ImageFilter.SMOOTH,
                                       ImageFilter.SHARPEN],
                        'fadedpicture':[ImageFilter.EMBOSS,
                                       ImageFilter.CONTOUR ,
                                       ImageFilter.SMOOTH,
                                       ImageFilter.SHARPEN,
                                       ImageFilter.DETAIL,
                                       ImageFilter.EDGE_ENHANCE],
                         'colorpencil':[ImageFilter.DETAIL,
                                       ImageFilter.SMOOTH_MORE ,
                                       ImageFilter.EDGE_ENHANCE,
                                       ImageFilter.SMOOTH_MORE,
                                       ImageFilter.CONTOUR],
                            'tinstamp':[ImageFilter.EDGE_ENHANCE,
                                       ImageFilter.EMBOSS ,
                                       ImageFilter.DETAIL],
                     'contrastdrawing':[ImageFilter.CONTOUR,
                                       ImageFilter.DETAIL,
                                       ImageFilter.SMOOTH],
                          'staticwash':[ImageFilter.EDGE_ENHANCE,
                                       ImageFilter.SMOOTH,
                                       ImageFilter.EDGE_ENHANCE,
                                       ImageFilter.CONTOUR,
                                       ImageFilter.SHARPEN,
                                       ImageFilter.FIND_EDGES,
                                       ImageFilter.SMOOTH,
                                       ImageFilter.EDGE_ENHANCE,
                                       ImageFilter.CONTOUR,
                                       ImageFilter.SMOOTH],
                         'staticwash2':[ImageFilter.EDGE_ENHANCE,
                                       ImageFilter.EDGE_ENHANCE_MORE,
                                       ImageFilter.CONTOUR,
                                       ImageFilter.SHARPEN,
                                       ImageFilter.FIND_EDGES,
                                       ImageFilter.EDGE_ENHANCE,
                                       ImageFilter.CONTOUR,
                                       ImageFilter.SMOOTH,
                                       ImageFilter.SMOOTH,
                                       ImageFilter.SMOOTH],
                'blackvelvetpainting6':[ImageFilter.SMOOTH_MORE,
                                       ImageFilter.DETAIL ,
                                       ImageFilter.SHARPEN,
                                       ImageFilter.FIND_EDGES],
    }

    # https://blog.furas.pl/python-tkinter-how-to-load-display-and-replace-image-on-label-button-or-canvas-gb.html
    # button image from link above
    straight_face_button_image_gif_b64='''
      iVBORw0KGgoAAAANSUhEUgAAACMAAAAjAQMAAAAkFyEaAAAABlBMVEX///8AAABVwtN+AAAAJ0lE
      QVQI12P4DwQPGCDkAQYGhgRSSDv+BjwkqabZ/2/AQ+LVi+QLAGveQwjt4H11AAAAAElFTkSuQmCC
      '''

    smiley_face_button_image_gif_b64='''\
      R0lGODdhIwAjAAAAACwAAAAAIwAjAIcAAAAAADMAAGYAAJkAAMwAAP8AKwAAKzMAK2YAK5kAK8wA
      K/8AVQAAVTMAVWYAVZkAVcwAVf8AgAAAgDMAgGYAgJkAgMwAgP8AqgAAqjMAqmYAqpkAqswAqv8A
      1QAA1TMA1WYA1ZkA1cwA1f8A/wAA/zMA/2YA/5kA/8wA//8zAAAzADMzAGYzAJkzAMwzAP8zKwAz
      KzMzK2YzK5kzK8wzK/8zVQAzVTMzVWYzVZkzVcwzVf8zgAAzgDMzgGYzgJkzgMwzgP8zqgAzqjMz
      qmYzqpkzqswzqv8z1QAz1TMz1WYz1Zkz1cwz1f8z/wAz/zMz/2Yz/5kz/8wz//9mAABmADNmAGZm
      AJlmAMxmAP9mKwBmKzNmK2ZmK5lmK8xmK/9mVQBmVTNmVWZmVZlmVcxmVf9mgABmgDNmgGZmgJlm
      gMxmgP9mqgBmqjNmqmZmqplmqsxmqv9m1QBm1TNm1WZm1Zlm1cxm1f9m/wBm/zNm/2Zm/5lm/8xm
      //+ZAACZADOZAGaZAJmZAMyZAP+ZKwCZKzOZK2aZK5mZK8yZK/+ZVQCZVTOZVWaZVZmZVcyZVf+Z
      gACZgDOZgGaZgJmZgMyZgP+ZqgCZqjOZqmaZqpmZqsyZqv+Z1QCZ1TOZ1WaZ1ZmZ1cyZ1f+Z/wCZ
      /zOZ/2aZ/5mZ/8yZ///MAADMADPMAGbMAJnMAMzMAP/MKwDMKzPMK2bMK5nMK8zMK//MVQDMVTPM
      VWbMVZnMVczMVf/MgADMgDPMgGbMgJnMgMzMgP/MqgDMqjPMqmbMqpnMqszMqv/M1QDM1TPM1WbM
      1ZnM1czM1f/M/wDM/zPM/2bM/5nM/8zM////AAD/ADP/AGb/AJn/AMz/AP//KwD/KzP/K2b/K5n/
      K8z/K///VQD/VTP/VWb/VZn/Vcz/Vf//gAD/gDP/gGb/gJn/gMz/gP//qgD/qjP/qmb/qpn/qsz/
      qv//1QD/1TP/1Wb/1Zn/1cz/1f///wD//zP//2b//5n//8z///8AAAAAAAAAAAAAAAAI/wABCBxI
      sKDBgwgTKlxo0J7DhxAjSpz4kKA9eBczYtyosSPHj/YsZnSIkeTDkiNTogw5cORKiS8hltwoMqXH
      myBNshTo0uRMnzp/ZhQptKjMoDotGu3ZkelMokmh7uTJtObPgi6x6ryodKvWkgU5jpRK0+pUACdN
      dk0ZdixBsWBb9oy5FabagShf5gQJ1yHZpoDzboW31qjgpW6pClUZ0TDJt3cBOEYcV7FfnpTrPsUb
      Oe3PzYKnekVLF2JLwZCzotX4EaNcsX9ZIq24mnFqm3LVabTc9G/lg7OHnq5Lu2baqLz54mx6lbPT
      44xnx3Y8N2jqxYuZVmXIvbv37wACAgA7
      '''

    blushy_face_button_image_gif_b64='''\
      R0lGODdhIwAjAAAAACwAAAAAIwAjAIcAAAAAADMAAGYAAJkAAMwAAP8AKwAAKzMAK2YAK5kAK8wA
      K/8AVQAAVTMAVWYAVZkAVcwAVf8AgAAAgDMAgGYAgJkAgMwAgP8AqgAAqjMAqmYAqpkAqswAqv8A
      1QAA1TMA1WYA1ZkA1cwA1f8A/wAA/zMA/2YA/5kA/8wA//8zAAAzADMzAGYzAJkzAMwzAP8zKwAz
      KzMzK2YzK5kzK8wzK/8zVQAzVTMzVWYzVZkzVcwzVf8zgAAzgDMzgGYzgJkzgMwzgP8zqgAzqjMz
      qmYzqpkzqswzqv8z1QAz1TMz1WYz1Zkz1cwz1f8z/wAz/zMz/2Yz/5kz/8wz//9mAABmADNmAGZm
      AJlmAMxmAP9mKwBmKzNmK2ZmK5lmK8xmK/9mVQBmVTNmVWZmVZlmVcxmVf9mgABmgDNmgGZmgJlm
      gMxmgP9mqgBmqjNmqmZmqplmqsxmqv9m1QBm1TNm1WZm1Zlm1cxm1f9m/wBm/zNm/2Zm/5lm/8xm
      //+ZAACZADOZAGaZAJmZAMyZAP+ZKwCZKzOZK2aZK5mZK8yZK/+ZVQCZVTOZVWaZVZmZVcyZVf+Z
      gACZgDOZgGaZgJmZgMyZgP+ZqgCZqjOZqmaZqpmZqsyZqv+Z1QCZ1TOZ1WaZ1ZmZ1cyZ1f+Z/wCZ
      /zOZ/2aZ/5mZ/8yZ///MAADMADPMAGbMAJnMAMzMAP/MKwDMKzPMK2bMK5nMK8zMK//MVQDMVTPM
      VWbMVZnMVczMVf/MgADMgDPMgGbMgJnMgMzMgP/MqgDMqjPMqmbMqpnMqszMqv/M1QDM1TPM1WbM
      1ZnM1czM1f/M/wDM/zPM/2bM/5nM/8zM////AAD/ADP/AGb/AJn/AMz/AP//KwD/KzP/K2b/K5n/
      K8z/K///VQD/VTP/VWb/VZn/Vcz/Vf//gAD/gDP/gGb/gJn/gMz/gP//qgD/qjP/qmb/qpn/qsz/
      qv//1QD/1TP/1Wb/1Zn/1cz/1f///wD//zP//2b//5n//8z///8AAAAAAAAAAAAAAAAI/wABCBxI
      sKDBgwgTKlxo0J7DhxAjSpz4kKA9eBczYtyosSPHj/YsZnSIkeTDkiNTogw5cORKiS8hltwoMqXH
      myBNshTo0uRMnzp/ZhQptKjMoDotGu3ZkelMokmh7uTJtObPgi6x6ryodKvWkgU5jpRK0+pUACdN
      dk0ZdixBsWBb9oy5FabagShf5gQJ16HIafDgAZ6msrBDwILtEYanVHDgVz/zMkUM2a9cyNMQG057
      MZXgbIG54rWnDh42zEb7BsbmmfBUkogBO+UcOHZZgRgJe4aXKm1kkgB0B+79mi1auhBbSn4blOrG
      jxjliiVrGWlFtFujj64rV51G50CL/yo++zX7a6ERG0aULB4oX5xImc82Tz8u+Pl9mz7djh4906oM
      BSjggAQCEBAAOw==
      '''

    yellow_caution_image_ico_b64 = '''
      R0lGODlhEAAQALMAAAAAAP//AP///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
      AAAAAAAAAAAA\nAAAAACH5BAEAAAIALAAAAAAQABAAQAQ3UMgpAKC4hm13uJnWgR
      TgceZJllw4pd2Xpagq0WfeYrD7\n2i5Yb+aJyVhFHAmnazE/z4tlSq0KIgA7\n
      '''


    false_2061132_1280_png_b64='''\
      iVBORw0KGgoAAAANSUhEUgAABQAAAAUACAYAAAAY5P/3AAEAAElEQVR42uzdeZxlV1X3/+/a+9xb
      Y48ZMBAyp0lVdVVoMjAlhEEFYjDpfkQRf4g48MiQjjiCIBBAVFQe0yGCiIJgUBSSIBERBSEEMAO0
      qeqqSkImIiSQdHqq8d579l6/P+6t7urOQNJd3V3D5/165ZWkp+o695y9115n7b0kAAAAAAAAAAAA
      AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
      AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
      AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
      AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
      AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
      AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
      AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
      AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
      AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
      AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
      AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
      AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
      AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
      AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
      AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
      AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
      AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
      AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
      AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
      AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
      AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
      AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADmL+MSAAAAHF7eisku
      l+ziWT9+s2RnzvzPxRfr/nvusWOsFb65Syec4Lr88r3+rJslnSn5gfx99vq6LfdfdJEdk/Oe/3fX
      MbO+/r5f93JJF7f+3w7w7wMAAIADQwIQAADgIMRY/vB4y6S9E2nTu3ZZ+1e+kiXlxZokayU3w/Tz
      nx/aly93Sbo/BB1zzTW+55fs+bft/WMAAACYi+CUSwAAAPDYfO8knunii6V77zV99rPe/Gn5gSbw
      vKenTZ2dnZqc7JR7u0KoSKoqxua/parcq7v/W2pTjB1KqUNSu9z3/B3NOvf+w73zMeI+l9nkXv/v
      PqWZ78fMJU0rxinlPCn3uqTmP2Z7/julhqS6cm7IbFpTU5Pq6Ji00dHaHFz75j8XXmg67riZqsOZ
      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
      AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
      AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
      AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
      AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
      AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
      AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
      AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
      AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
      AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
      AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
      AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
      AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
      AAAAAAAAAAAAAAA4m/1/neGEtRGM30cAAAAASUVORK5CYII=
      '''
#-------------------------------------------------------------------------------
#
# main
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_args(name, description):
  parser = argparse.ArgumentParser(prog=name, description=description, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('targets', help="Files sources", nargs='*')
  parser.add_argument('-l', '--loglevel', default="Warn", help="Set logging level.")
  parser.add_argument('-t', '--tracelevel', default=0, help="Set trace level.")
  switches = parser.parse_args()
  args=vars(switches)
  arguments = {'name': name, 'description': description}
  for arg in args:
    arguments[arg] = getattr(switches, arg)
    if arguments[arg] == None:
      del arguments[arg]
  for key, value in arguments.items():
    if type(value) is str:
      if value.upper() == 'TRUE':
        arguments[key] = True
      if value.upper() == 'FALSE':
        arguments[key] = False

  return arguments, switches

def main(name, description):
  params, switches = get_args(name, description)
  setloglevel(params['loglevel'])
  settracelevel(int(params['tracelevel']))
  if gettracelevel() > 0: logmainentry(name)
  loginfo(params)

  try:
    app = Cutie(params['targets'], showfile=False, inspector=True, debug=False)
    app.mainloop()
  except KeyboardInterrupt as e:
    pass

  if gettracelevel() > 0: logmainexit(name)

if __name__ == "__main__":
  main("Cutie", "Python Image Viewer")

#-------------------------------------------------------------------------------
#
# <|:) Wizard
#
#-------------------------------------------------------------------------------
