from matplotlib import pyplot as plt


def plot_order_flow(book_state_sequence, price_sequence=None, volumes_sequence=None, buy_sequence=None, sell_sequence=None):

    # Step 1: plot the order book in each timestep

    # Get Bid and Ask data in two different lists
    ask_data = [item for sublist in book_state_sequence for item in sublist if item[3] == 'ask']
    bid_data = [item for sublist in book_state_sequence for item in sublist if item[3] == 'bid']

    # get volumes and prices
    ask_times, ask_prices, ask_volumes = zip(*[(d[0], d[1], d[2]) for d in ask_data])
    bid_times, bid_prices, bid_volumes = zip(*[(d[0], d[1], d[2]) for d in bid_data])

    # Normalise the volumes
    max_volume = max(max(ask_volumes), max(bid_volumes))
    norm_ask_volumes = [v / max_volume for v in ask_volumes]
    norm_bid_volumes = [v / max_volume for v in bid_volumes]

    fig, ax = plt.subplots()

    # Plot the asks
    for t, p, v in zip(ask_times, ask_prices, norm_ask_volumes):
        ax.bar(t, v, width=1, bottom=p, color='blue', alpha=0.6)

    # plot the bids
    for t, p, v in zip(bid_times, bid_prices, norm_bid_volumes):
        ax.bar(t, -v, width=1, bottom=p, color='red', alpha=0.6)

    # add some gridlines
    prices = sorted(set(ask_prices + bid_prices))
    for price in prices:
        ax.axhline(y=price, color='grey', linestyle='--', linewidth=0.5)

    # axes labels
    ax.set_xlabel('Time')
    ax.set_ylabel('Price')
    ax.set_title('Ask and Bid Prices with Volumes')

    # set axes limits
    ax.set_xlim(min(ask_times + bid_times), max(ask_times + bid_times))

    # Step 2: plot the prices
    
    if price_sequence:
        x, y = zip(*[[i + 1, v] for (i, v) in enumerate(price_sequence)])
        ax.plot(x, y, color='orange', label='price')


        if volumes_sequence and buy_sequence and sell_sequence:
            ax.scatter(x, y, s=[val * 20 for val in [v * b for v,b in zip(volumes_sequence, buy_sequence)]], alpha=1, edgecolors='black', color='green')
            ax.scatter(x, y, s=[val * 20 for val in [v * s for v,s in zip(volumes_sequence, sell_sequence)]], alpha=1, edgecolors='black', color='red')

        ax.legend(loc='upper right')

    plt.show()