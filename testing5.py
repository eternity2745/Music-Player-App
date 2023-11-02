from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.navigationrail import MDNavigationRail, MDNavigationRailItem


class Example(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        return (
            MDBoxLayout(
                MDNavigationRail(
                    MDNavigationRailItem(
                        text="Python",
                        icon="language-python",
                    ),
                    MDNavigationRailItem(
                        text="JavaScript",
                        icon="language-javascript",
                    ),
                    MDNavigationRailItem(
                        text="CPP",
                        icon="language-cpp",
                    ),
                    MDNavigationRailItem(
                        text="Git",
                        icon="git",
                    ),
                )
            )
        )


Example().run()
