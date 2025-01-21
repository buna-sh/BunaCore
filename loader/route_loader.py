import os
import importlib
from colorama import Fore, init

# Initialize colorama
init(autoreset=True)

# Create a function to log messages with colors
def log_info(message):
    print(Fore.GREEN + "[INFO] " + message)

def log_error(message):
    print(Fore.RED + "[ERROR] " + message)

def log_warning(message):
    print(Fore.YELLOW + "[WARNING] " + message)

# Load modules dynamically from the ./routes directory
def load_routes(app):
    routes_dir = './routes'

    # Check if the directory exists
    if not os.path.exists(routes_dir):
        log_error("Routes directory does not exist!")
        return

    # Get all Python files in the routes directory
    for filename in os.listdir(routes_dir):
        if filename.endswith('.py'):
            route_name = filename[:-3]  # Remove '.py' extension
            log_info(f"Loading route module: {route_name}")

            try:
                # Dynamically import the route module
                module = importlib.import_module(f'routes.{route_name}')
                
                # Initialize the routes in the module
                module.init_app(app)
                log_info(f"Route {route_name} loaded successfully.")
            except Exception as e:
                log_error(f"Failed to load route {route_name}: {e}")
