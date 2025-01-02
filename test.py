import pygame  
import sys  
import numpy as np  
  
def create_plot(data_x, data_y):  
    import matplotlib  
    matplotlib.use('Agg')  # Use 'Agg' backend for rendering  
    import matplotlib.pyplot as plt  
    from matplotlib.backends.backend_agg import FigureCanvasAgg  
  
    fig, ax = plt.subplots(figsize=(8, 6), dpi=100)  
  
    # Plot your data  
    ax.plot(data_x, data_y, marker='o', linestyle='-', color='blue', linewidth=2)  
  
    # Set fixed y-axis limits from 35 to 45  
    y_min = 35  
    y_max = 45  
    ax.set_ylim(y_min, y_max)  
  
    # Disable autoscaling on y-axis  
    ax.autoscale(enable=False, axis='y')  
  
    # Set y-axis ticks at every 1 unit  
    y_ticks = range(y_min, y_max + 1, 1)  
    ax.set_yticks(y_ticks)  
    ax.yaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%d'))  
  
    # Enable grid lines on y-axis  
    ax.grid(True, which='major', axis='y', linestyle='--', linewidth=0.5)  
  
    # Set labels and title  
    ax.set_xlabel("Time (Weeks)")  
    ax.set_ylabel("Price")  
    ax.set_title("Price Over Time")  
  
    # Render the figure to a canvas  
    canvas = FigureCanvasAgg(fig)  
    canvas.draw()  
  
    # Get the RGB buffer from the figure  
    raw_data = canvas.tostring_argb()  
    width, height = canvas.get_width_height()  
  
    # Convert to a Pygame image  
    plot_surface = pygame.image.frombytes(raw_data, (width, height), "ARGB")  
  
    plt.close(fig)  
    return plot_surface  
  
def main():  
    pygame.init()  
    screen = pygame.display.set_mode((800, 600))  
    pygame.display.set_caption("Plot with Fixed Y-Axis")  
    clock = pygame.time.Clock()  
    running = True  
  
    # Initialize data  
    prices = [39, 39, 40, 40, 40, 38, 38, 38]  
    data_x = list(range(len(prices)))  
    plot_surface = create_plot(data_x, prices)  
  
    while running:  
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                running = False  
  
            # Example: Update plot when space key is pressed  
            elif event.type == pygame.KEYDOWN:  
                if event.key == pygame.K_SPACE:  
                    # Simulate adding a new data point  
                    new_price = 38 + np.random.choice([0, 1, 2])  
                    prices.append(new_price)  
                    data_x = list(range(len(prices)))  
                    plot_surface = create_plot(data_x, prices)  
  
        # Display the plot  
        screen.fill((255, 255, 255))  
        scaled_surface = pygame.transform.smoothscale(plot_surface, screen.get_size())  
        screen.blit(scaled_surface, (0, 0))  
        pygame.display.flip()  
        clock.tick(60)  
  
    pygame.quit()  
    sys.exit()  
  
if __name__ == "__main__":  
    main()  