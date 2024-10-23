from robocorp.tasks import task
from robocorp import browser

from RPA.HTTP import HTTP
from RPA.Tables import Tables

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