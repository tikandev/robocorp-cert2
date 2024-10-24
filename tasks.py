from robocorp.tasks import task
from robocorp import browser

from RPA.HTTP import HTTP
from RPA.Tables import Tables
from RPA.PDF import PDF
from RPA.Archive import Archive

@task
def order_robots_from_RobotSpareBin():
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """
    # Adding a slowmo effect to the robot so viewing test results becomes easier
    browser.configure(
        slowmo=100,
    )
    open_robot_order_website()
    orders = get_orders()

    close_annoying_modal()

    for row in orders:
        fill_the_form(row)

    archive_receipts()
    

def open_robot_order_website():
    # Getting the robot to open the correct website
    browser.goto("https://robotsparebinindustries.com/#/robot-order")

def get_orders():
    # Downloading the .csv file containing the order information, overwriting enabled
    http = HTTP()
    http.download(url="https://robotsparebinindustries.com/orders.csv", target_file="output/orders.csv", overwrite=True)
    ordertable = Tables().read_table_from_csv("output/orders.csv", columns=["Order number", "Head", "Body", "Legs", "Address"])
    return ordertable

def close_annoying_modal():
    # Get's rid of the popup on the site
    page = browser.page()
    page.click("button:text('OK')")

def fill_the_form(order):
    # Fills the form with data from orders.csv
    page = browser.page()
    page.select_option("select#head", value=order['Head'])
    id_body = "id-body-" + order['Body']
    page.set_checked(f"#{id_body}", checked=True)
    page.get_by_placeholder("Enter the part number for the legs").fill(value=order['Legs'])
    page.fill("#address", value=order['Address'])
    submit_the_form(order)

def order_another_robot():
    # After completing the order the page loads again and changes. Finds the button to start the order process agains and clicks it
    page = browser.page()
    page.click("button:text('ORDER ANOTHER ROBOT')")

def submit_the_form(order):
    # Submits the filled form and handles exceptions
    page = browser.page()
    while True:
        page.click("button:text('ORDER')")
        order_another = page.query_selector("button:text('ORDER ANOTHER ROBOT')")
        if order_another:
            pdf_path = store_receipt_as_pdf(order)
            screenshot_path = screenshot_robot(order)
            embed_screenshot_to_receipt(screenshot_path,pdf_path)
            order_another_robot()
            close_annoying_modal()
            break

def store_receipt_as_pdf(order_number):
    # Creates a pdf of the order confirmation pages receipt
    page = browser.page()
    order_confirmation_html = page.locator("#receipt").inner_html()
    pdf = PDF()
    pdf_path = f"output/receipts/order_receipt{order_number['Order number']}.pdf"
    pdf.html_to_pdf(order_confirmation_html, pdf_path)
    return pdf_path

def screenshot_robot(order_number):
    # Takes a screenshot of the ordered robot
    page = browser.page()
    robot_picture = page.locator("#robot-preview-image")
    screenshot_path = f"output/screenshots/screenshot{order_number['Order number']}.png"
    robot_picture.screenshot(path=screenshot_path)
    return screenshot_path

def embed_screenshot_to_receipt(screenshot_path, pdf_path):
    # Adds screenshot of the ordered robot to the receipt pdf
    pdf = PDF()
    pdf.add_watermark_image_to_pdf(screenshot_path, pdf_path, pdf_path)

def archive_receipts():
    # Archivces generated receipts as a .zip
    zip_file = Archive()
    zip_file.archive_folder_with_zip("./output/receipts", "./output/receipts.zip")