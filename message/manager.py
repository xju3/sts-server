import os
from typing import Dict, Set
from flask_socketio import SocketIO, emit, join_room, leave_room

class SocketManager:
    def __init__(self, socketio: SocketIO):
        """
        Initialize SocketManager with SocketIO instance
        
        :param socketio: Flask-SocketIO instance
        """
        self.socketio = socketio
        
        # Global dictionaries to track connections, rooms, and users
        self.connected_clients: Dict[str, str] = {}  # {sid: client_id}
        self.rooms: Dict[str, Set[str]] = {}  # {room_name: {client_ids}}
        self.client_sessions: Dict[str, str] = {}  # {client_id: current_room}
        
        # Register socket event handlers
        self.register_handlers()

    
    def register_handlers(self):
        """
        Register all socket event handlers
        """
        self.socketio.on_event('verify_client', self.verify_client)
        self.socketio.on_event('create_room', self.create_room)
        self.socketio.on_event('join_room', self.join_room)
        self.socketio.on_event('send_message', self.send_message)
        self.socketio.on_event('list_rooms', self.list_rooms)
        self.socketio.on_event('disconnect', self.handle_disconnect)
        self.socketio.on_event('on_review_finished', self.handle_disconnect)
    

    def on_review_finished(self, data):
        """ send the review messages to students """
        client_id = data.get("client_id")
        sid = self.find_sid_by_client_id(client_id)
        if sid is None:
            return

        review_info = data.get("review_info")
        pass


    def find_sid_by_client_id(self, client_id: str) -> str:
        """
        Finds the socket ID (sid) associated with a given client ID.

        Args:
            client_id: The ID of the client.

        Returns:
            The socket ID (sid) if found, otherwise None.
        """
        for sid, c_id in self.connected_clients.items():
            if c_id == client_id:
                return sid
        return None


    def verify_client(self, data):
        """
        Verify client connection by checking client_id
        
        :param data: Dictionary containing client_id
        """
        sid = self.socketio.server.sid
        client_id = data.get('client_id')
        
        # Validate client ID
        if not client_id:
            emit('connection_error', {
                'message': 'Client ID is required to connect'
            })
            return False
        
        # Check if client ID is already connected
        if client_id in self.connected_clients.values():
            emit('connection_error', {
                'message': 'This client ID is already in use'
            })
            return False
        
        # Store connection information
        self.connected_clients[sid] = client_id
        
        # Confirm successful connection
        emit('connection_verified', {
            'message': 'Successfully connected',
            'client_id': client_id
        })
        
        print(f"Client verified - SID: {sid}, Client ID: {client_id}")
    
    def handle_disconnect(self):
        """
        Handle client disconnections
        """
        sid = self.socketio.server.sid
        
        # Remove from connected clients
        if sid in self.connected_clients:
            client_id = self.connected_clients[sid]
            
            # Remove from current room if in one
            if client_id in self.client_sessions:
                current_room = self.client_sessions[client_id]
                
                # Remove client from room
                if current_room in self.rooms and client_id in self.rooms[current_room]:
                    self.rooms[current_room].discard(client_id)
                    
                    # Broadcast leave message
                    emit('room_message', {
                        'client_id': client_id,
                        'message': f'Client {client_id} has left the room.',
                        'room': current_room
                    }, room=current_room)
                    
                    # Clean up empty rooms
                    if not self.rooms[current_room]:
                        del self.rooms[current_room]
                
                # Remove from client sessions
                del self.client_sessions[client_id]
            
            # Remove from connected clients
            del self.connected_clients[sid]
    
    def create_room(self, data):
        """
        Create a new chat room
        
        :param data: Dictionary containing room details
        """
        sid = self.socketio.server.sid
        
        # Verify client is connected
        if sid not in self.connected_clients:
            emit('connection_error', {
                'message': 'You must verify your client ID first'
            })
            return
        
        client_id = self.connected_clients[sid]
        room_name = data.get('room') or f"room_{len(self.rooms) + 1}"
        
        # Ensure unique room name
        base_room_name = room_name
        counter = 1
        while room_name in self.rooms:
            room_name = f"{base_room_name}_{counter}"
            counter += 1
        
        # Create room and add client
        self.rooms[room_name] = {client_id}
        self.client_sessions[client_id] = room_name
        
        # Join the room
        join_room(room_name)
        
        # Emit room creation confirmation
        emit('room_joined', {
            'room': room_name,
            'client_id': client_id,
            'message': f'Room {room_name} created successfully.'
        })
        
        # Broadcast room creation
        emit('room_message', {
            'client_id': client_id,
            'message': f'Client {client_id} created the room.',
            'room': room_name
        }, room=room_name)
    
    def join_room(self, data):
        """
        Join an existing chat room
        
        :param data: Dictionary containing room details
        """
        sid = self.socketio.server.sid
        
        # Verify client is connected
        if sid not in self.connected_clients:
            emit('connection_error', {
                'message': 'You must verify your client ID first'
            })
            return
        
        client_id = self.connected_clients[sid]
        room_name = data.get('room')
        
        # Validate room
        if not room_name:
            emit('error', {'message': 'Room name is required'})
            return
        
        if room_name not in self.rooms:
            emit('error', {'message': 'Room does not exist'})
            return
        
        # Leave previous room if in one
        if client_id in self.client_sessions:
            previous_room = self.client_sessions[client_id]
            if previous_room in self.rooms:
                self.rooms[previous_room].discard(client_id)
                leave_room(previous_room)
        
        # Join new room
        self.rooms[room_name].add(client_id)
        self.client_sessions[client_id] = room_name
        join_room(room_name)
        
        # Emit join confirmation
        emit('room_joined', {
            'room': room_name,
            'client_id': client_id,
            'message': f'Joined room {room_name} successfully.'
        })
        
        # Broadcast user joined message
        emit('room_message', {
            'client_id': client_id,
            'message': f'Client {client_id} has joined the room.',
            'room': room_name
        }, room=room_name)
    
    def send_message(self, data):
        """
        Handle and broadcast chat messages
        
        :param data: Dictionary containing message details
        """
        sid = self.socketio.server.sid
        
        # Verify client is connected
        if sid not in self.connected_clients:
            emit('connection_error', {
                'message': 'You must verify your client ID first'
            })
            return
        
        client_id = self.connected_clients[sid]
        room = data.get('room')
        message = data.get('message', '').strip()
        
        if not room or not message:
            return
        
        # Verify client is in the room
        if client_id not in self.client_sessions or self.client_sessions[client_id] != room:
            emit('error', {'message': 'You are not in this room'})
            return
        
        # Broadcast message to the room
        emit('room_message', {
            'client_id': client_id,
            'message': message,
            'room': room
        }, room=room)
    
    def list_rooms(self, data=None):
        """
        List all available chat rooms
        
        :param data: Optional data parameter (not used)
        """
        sid = self.socketio.server.sid
        
        # Verify client is connected
        if sid not in self.connected_clients:
            emit('connection_error', {
                'message': 'You must verify your client ID first'
            })
            return
        
        room_list = [
            {
                'room': room, 
                'members': len(members)
            } for room, members in self.rooms.items()
        ]
        emit('room_list', {'rooms': room_list})