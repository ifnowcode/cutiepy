# Cutie Image Viewer

Cutie is a feature‑rich, Tkinter‑based image and video viewer that supports slideshows, filters, effects, GIF frame inspection, window geometry modes, transparency, desktop wallpaper integration, and a command console.
It uses **Pillow**, **OpenCV**, and **Tkinter** to provide a highly interactive viewing environment.

This is highly experimental code currently. I am working on cleaning this up since it's a nice viewer that uses a directory tree (will display all images from selected folder on down). This was created for that reason and to explore Pillow and OpenCV. I don't believe I ever got the OpenCV functionality working but I'll dive back into that when time permits. The image viewing portion works well, the rest I'm not so sure, it has a lot of functionality due to Pillow and image generation exploration. If OpenCV is not needed here I'll remove it in future iterations.

I created this readme from AI but will clean up as much as I can time permitting making sure all the info is accurate and useful.

When you provide a path it will crawl it for images to display which make take a while depending on the size or you can pass it file(s) to display.

I left all the links and notes in the code since this is about learning PIL and because this is very much experimental RnD.

I'm in the process of changing how the command line is processed so  `process_command_line_arguments` needs to be cleaned up and renamed.

This was an early project in my Python learning curve so it's currently a bit of a mess but it works.
---

## Features

### Image & Video Support

  * Loads: JPG, PNG, BMP, GIF, WEBP, WEBM, TIFF, ICO, PPM, Base64 (`*.b64`)

  * Plays videos via OpenCV: MPG, MP4, AVI, FLV, MOV

  * GIF frame navigation tool (`[` key)

### Image Processing

  * Full suite of Pillow filters (blur, contour, detail, sharpen, emboss, edges, smooth, grayscale)

  * Random filter generation

  * Aggregate filter generation

  * Thumbnail mode

  * Crop to bounding box

  * Zooming and transparency control

  * Image info overlay (filename + color)

### Window Modes

  * Tool mode

  * Widget mode

  * Compact

  * Normal

  * Widescreen

  * Fullscreen

  * Zoomed window

  * Desktop wallpaper mode (sets Windows wallpaper)

### Slideshow

  * Adjustable interval

  * Repeat mode

  * Random mode

  * Shuffle mode

  * Directory navigation (PageUp/PageDown)

### Command Console

  * Full command interpreter (`CMD::`)

  * History navigation

  * Filter commands

  * Resize/original commands

  * Dumping sources

  * Geometry switching

  * Wallpaper style control

---

## Keyboard Shortcuts

  * Alt + Up — Move window up

  * Alt + Down — Move window down

  * Alt + Left — Move window left

  * Alt + Right — Move window right

  * Ctrl + Up — Move window up (fast)

  * Ctrl + Down — Move window down (fast)

  * Ctrl + Left — Move window left (fast)

  * Ctrl + Right — Move window right (fast)

  * Alt + c — Center window

### Function Keys

#### General

  * F1 — Help

  * F2 — Toggle widgets

  * F3 — Toggle zoom mode

  * F4 — Crop image

  * F5 — Draw image info

  * F6 — Background: slate

  * F7 — Background: white

  * F8 — Background: black

  * F9 — Toggle transparency

  * F10 — Set wallpaper

  * F11 — Toggle test flag

  * F12 — Toggle debug + diagnostics tool

### Shift + Function Keys

  * Shift + F2 — Play/pause slideshow

### Alt + Function Keys (Window Geometry Modes)

  * Alt + F1 — Iconify

  * Alt + F2 — Minimize

  * Alt + F3 — Maximize

  * Alt + F5 — Tool mode

  * Alt + F6 — Widget mode

  * Alt + F7 — Compact mode

  * Alt + F8 — Normal mode

  * Alt + F9 — Widescreen mode

  * Alt + F10–F12 — Disabled (prevent accidental toggles)

### Picture Navigation

  * Left Arrow — Previous image

  * Right Arrow — Next image

  * Up Arrow — Decrease slideshow interval

  * Down Arrow — Increase slideshow interval

  * Space — Start/stop slideshow

  * Home — First slide

  * End — Last slide

  * PageUp (Prior) — Previous directory

  * PageDown (Next) — Next directory

  * Escape — Exit fullscreen / reset window on double‑tap

  * f — Fullscreen

  * r — Random image

  * l — Toggle repeat

  * z — Toggle random/sequential

  * q — Toggle shuffle

### Image Modes

  * o — Original size

  * w — Resize to window

  * s — Toggle resize

  * t — Toggle thumbnail mode

  * j — Desktop wallpaper mode

  * u — Toggle menu

  * . — Toggle command tool

  * [ — Toggle GIF frame tool

### Filters & Effects

#### Quick Filters

  * v — Privacy mode (100px Gaussian blur)

  * y — Grayscale

  * b — Blur

  * c — Contour

  * d — Detail

  * e — Emboss

  * h — Edge enhance

  * p — Sharpen

  * m — Smooth

  * g — Find edges

  * i — Toggle selected filters

  * x — Clear all filters

  * k — Toggle effects (spread effect)

### Filter Generation

  * n — New random filter

  * a — New aggregate filter

### Zoom & Transparency

  * = — Zoom in

  * - — Zoom out

  * Shift + + — Increase alpha (window transparency)

  * Shift + _ — Decrease alpha

### Developer / Diagnostic

  * Alt + 1–0 — Generate test images

  * Alt + F1–F3 — Window control

  * Debug mode exposes diagnostic toolbar

### Command Console (CMD::)

Commands typed into the console (opened with `.`) include:

#### Filter Commands

  * toggle blur

  * add blur

  * remove blur

  * … (all filters supported)

#### Image Commands

  * resize image

  * origional image

  * random image

  * interval <seconds>

  * home / end

  * up / down (directory navigation)

#### System Commands

  * debug

  * verb

  * trace

  * cls

  * geometry <mode>

  * picturepos <0–10>

  * dump sources

  * exit (close command tool)

#### Filter Shortcuts

  * `filter <name>` — Assign filter set to number key 0–9

  * Pressing that number key applies the filter set

---

## Installation

### Requirements

  * Python 3.x

  * Pillow

  * OpenCV (`cv2`)

  * Tkinter (bundled with Python on Windows)

  * Numpy

Install dependencies:

bash
```
pip install pillow opencv-python numpy
```

---

## Running

bash
```
python cutie.py <optional file or directory>
```

Examples:

bash
```
python cutie.py C:\Pictures
python cutie.py image.jpg
python cutie.py encoded.b64
```

---

Desktop Mode Notes

Cutie can **set your Windows wallpaper** dynamically:

  * Press j to toggle desktop mode

  * Press F10 to set wallpaper

  * Wallpaper style controlled via registry (`WallpaperStyle`, `TileWallpaper`)

  Note: This is a hack so use at your own risk. I developed this in Windows 8, still works to set but doesn't unset on exit or command in Windows 10.

---

## GIF Frame Tool

Press `[` to toggle the GIF frame inspector.

Displays:

Code
```
current_frame / total_frames
```

Allows stepping through frames with the frame tool buttons.

---

## Logging

Logs are written to:

Code
```
<self.module_path>\logs\cutiepy\pillowtalk_<timestamp>_log.txt
```