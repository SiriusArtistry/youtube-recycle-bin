from nicegui import ui, app
import random

@ui.page('/')
def main_page():
    random_10digit = "".join([str(random.randint(0, 9)) for _ in range(10)])
    app.storage.user['random_10digit'] = random_10digit
    ui.label(f"Random 10-digit number: {random_10digit}")
    ui.label(f"Do you find it in /.nicegui/storage-{app.storage.browser['id']}.json ?")

ui.run(storage_secret="Hello")