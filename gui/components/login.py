import flet as ft

async def login_page(page: ft.Page):
    page.window.bgcolor = "#2a2a2a"
    page.window.min_width = 800
    page.window.min_height = 600
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER


    page.add(
        ft.Row(
            controls=[
                ft.Container(expand=35),
                ft.Column(
                    controls=[
                        ft.Text(
                            "Dialox", 
                            text_align=ft.TextAlign.CENTER, 
                            color="#f0f0f0", 
                            size=70, 
                            weight=ft.FontWeight.W_900, 
                            no_wrap=True
                        ),
                        ft.TextField(
                            label="Input a email",
                            hint_text="dialox@exemple.com"
                        ),
                        ft.TextField(
                            label="Input a password",
                            password=True,
                            can_reveal_password=True
                        ),
                        ft.Row(
                            controls=[
                                ft.FilledButton(
                                    content=ft.Text(
                                        "login",
                                        size=24,
                                        weight=ft.FontWeight.BOLD,
                                        color="#f0f0f0"
                                    ),
                                    bgcolor="#3b82f6",
                                    height=40,
                                    expand=True
                                )
                            ],
                            expand=True
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                    expand=30
                ),
                ft.Container(expand=35)
            ]
        )
    )
