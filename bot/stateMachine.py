from typing import Callable


class StateMachine:
    def __init__(self):
        self._states = {}
        self._current_state_id = 0

    def addState(self, id: int, handler: Callable):
        self._states[id] = handler

    def handleState(self, message) -> bool:
        if self._current_state_id == 0 and len(self._states) == 0:
            return False
        
        handler = self._states.get(self._current_state_id)
        if handler == None:
            return False
        
        forceNextHandle = False
        h_res = handler(message, self._current_state_id)
        if isinstance(h_res, int):
            self._current_state_id = h_res
        else:
            self._current_state_id, forceNextHandle = h_res 

        if forceNextHandle:
            return self.handleState(message)
        
        return True
    
    def reset(self):
        self._current_state_id = 0

# class StateMachine:
#     def __init__(self, initial_handler: Callable):
#         self._current_handler = initial_handler
#         self._initial_handler = initial_handler

#     def handleState(self, message) -> bool:
#         if self._current_handler==None:
#             return False
        
#         forceNextHandle = False
#         h_res = self._current_handler(message, self._current_state_id)
#         if isinstance(h_res, tuple):
#             self._current_handler, forceNextHandle = h_res 
#         else:
#             self._current_handler = h_res

#         if forceNextHandle:
#             return self.handleState(message)
        
#         return True
    
#     def reset(self):
#         self._current_handler = self._initial_handler



