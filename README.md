# Client-Server Real-Time Chat Application
## Overview
A fully functional real-time chat application built from scratch in Python. The project consists of a multithreaded server that manages multiple simultaneous client connections and a feature-rich GUI client built with Tkinter. Designed to demonstrate core networking concepts including socket programming, concurrent connection handling, and real-time data exchange.

## Features
Messaging

Real-time broadcast messaging between all connected clients
Private messaging system using /pm <username> <message>
Typing notifications to indicate when a user is active
Timestamped messages for conversation tracking
@mention highlighting for direct references

User Management

Nickname registration on join with duplicate detection
Online users list via /online command
Clean disconnect handling with broadcast notification

GUI Client

Built with Tkinter — no external dependencies
Dark and light mode toggle
Multi-language support: English, Spanish, French, German, Chinese
Color-coded messages: sent, received, system, and mentions displayed differently
Send button cooldown to prevent message spam

Server

Handles multiple clients simultaneously using Python threading
Graceful error handling for unexpected disconnections
Built-in commands: /quit, /online, /help, /typing


## Tech Stack

Language: Python 3
Networking: socket module (TCP)
Concurrency: threading module
GUI: tkinter, scrolledtext


## Project Structure
├── server.py      # Multithreaded chat server
├── client1.py     # GUI chat client (instance 1)
├── client2.py     # GUI chat client (instance 2)
├── client3.py     # GUI chat client (instance 3)

## How to Run
Step 1 — Start the server
python server.py
Step 2 — Launch one or more clients
python client1.py
python client2.py
python client3.py
Each client connects to localhost:25000 by default.

## Commands
CommandDescription/pm <user> <message>Send a private message/onlineList all connected users/typingNotify others you are typing/quitDisconnect from the server/helpShow available commands

## What I Learned

How TCP sockets work in practice — connection, data transfer, disconnection
Managing multiple clients concurrently using threads
Building event-driven GUI applications with Tkinter
Structuring a client-server architecture from scratch
