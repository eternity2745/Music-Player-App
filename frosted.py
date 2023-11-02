
from kivy.lang import Builder
from kivy.app import App
from kivy.clock import Clock
from kivy_garden.frostedglass import FrostedGlass


KV = """
RelativeLayout:
    Image:
        id:bg
        source:app.image
        fit_mode:"cover"
        anim_delay:0.05 

    FrostedGlass:
        id:glass
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        size_hint: 0.5, 0.5
        background:bg
        blur_size: 45
        saturation: 1.0
        luminosity: 1.2
        noise_opacity: 0.05
        border_radius:  [dp(20)] * 4
        overlay_color:1,1,1,0.2
        outline_color: 1,1,1,0.2
        outline_width: dp(0.8)
"""


class Main(App):

    image = 'images/malikappuram.jpeg'

    def build(self):
        return Builder.load_string(KV)


Main().run()
