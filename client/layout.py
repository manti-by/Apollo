main_widget = '''
#:import ThemeManager kivymd.theming.ThemeManager
#:import MDNavigationDrawer kivymd.navigationdrawer.MDNavigationDrawer
#:import colors kivymd.color_definitions.colors
#:import Toolbar kivymd.toolbar.Toolbar

NavigationLayout:
    id: nav_layout
    MDNavigationDrawer:
        id: nav_drawer
        NavigationDrawerToolbar:
            title: 'Settings'
        NavigationDrawerIconButton:
            icon: 'home'
            text: 'Sensors'
            on_release: app.root.ids.screen_manager.current = 'sensors'
        NavigationDrawerIconButton:
            icon: 'cast-connected'
            text: 'Server address'
            on_release: app.show_server_address_dialog()
        NavigationDrawerIconButton:
            icon: 'qqchat'
            text: 'Bugtracker'
            on_release: lambda x: None
        NavigationDrawerIconButton:
            icon: 'information-outline'
            text: 'About'
            on_release: app.root.ids.screen_manager.current = 'about'

    BoxLayout:
        orientation: 'vertical'
        Toolbar:
            id: toolbar
            title: 'Apollo'
            background_color: app.theme_cls.primary_color
            left_action_items: [['menu', lambda x: app.root.toggle_nav_drawer()]]
        ScreenManager:
            id: screen_manager
            Screen:
                name: 'sensors'
                ScrollView:
                    do_scroll_x: False
                    MDList:
                        id: sensor_list
                        TwoLineListItem:
                            text: "Guest Room"
                            secondary_text: "23*C / 68%"
                        TwoLineListItem:
                            text: "Bath Room"
                            secondary_text: "27*C / 85%"
                        TwoLineListItem:
                            text: "Slipping Room"
                            secondary_text: "22*C / 74%"
            Screen:
                name: 'about'
                ScrollView:
                    BoxLayout:
                        orientation: 'vertical'
                        size_hint_y: None
                        height: self.minimum_height
                        padding: dp(48)
                        spacing: 20
                        MDLabel:
                            font_style: 'Title'
                            theme_text_color: 'Primary'
                            text: 'About this app'
                        MDLabel:
                            font_style: 'Body1'
                            theme_text_color: 'Primary'
                            text: 'Raspberry Pi IoT application for monitoring Arduino clients with DHT sensors via Wi-Fi. '

'''