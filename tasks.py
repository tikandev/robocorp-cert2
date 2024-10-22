from robocorp.tasks import task
from robocorp import browser

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

def open_robot_order_website():
    # Getting the robot to open the correct website
    browser.goto("https://robotsparebinindustries.com/#/robot-order")
