# Coffee shop manager

A small Python program that helps run a coffee and snack shop from the command line.

## Why I made it

I noticed that my uncle managed most of his shop's daily activities manually. Keeping track of customer orders, product prices, and daily sales could take extra time. I thought a simple computer program could make these tasks more organized and easier to manage.

The menu in the program uses the real items and prices from his shop, in Bangladeshi Taka.

## What it does

- Shows a menu and takes a customer's order
- Prints a bill with the total
- Saves every sale to `sales.csv` with the date and time
- Tracks coffee beans and milk, and takes them off the stock when a drink is sold
- Warns when stock is running low, and lets the owner restock
- Shows a sales report for today: number of orders, items sold, money earned, and the best seller

## How to run it

Install Python from python.org and put `coffee_shop.py` in a folder. Open a terminal in that folder and type `python coffee_shop.py`.

The program creates `sales.csv` and `stock.json` by itself the first time it saves something.

## What was hard

As a beginner in Python, understanding how different parts of the program work together was challenging for me. I especially needed time to understand how to save orders and retrieve previous order information correctly.

## What I learned

I learned how Python can be used to solve practical problems. Before this project, I mainly knew basic programming concepts. Now I understand how to use functions and lists, and how to read and write files, to build a small working application.

## What I would add next

I would like to add a simple graphical interface so that someone can use the system without typing commands. I would also like to improve the sales report and make the system easier to use for my uncle's shop.

## A note on how I built it

I used an AI assistant as a guide while learning, and I tested and changed the program myself.
