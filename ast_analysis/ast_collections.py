class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class Stack:
    def __init__(self):
        self.head = Node("head")
        self.size = 0

    def __str__(self):
        cur = self.head.next
        out = ""
        while cur:
            out += str(cur.value) + "->"
            cur = cur.next
        return out[:-2]

    def getSize(self) -> int:
        return self.size

    def isEmpty(self) -> bool:
        return self.size == 0

    def peek(self):
        if self.isEmpty():
            return None

        return self.head.value

    def push(self, value: any) -> None:
        node = Node(value)
        node.next = self.head
        self.head = node
        self.size += 1

    def pop(self) -> any:
        if self.isEmpty():
            raise Exception("Popping from an empty stack")
        remove = self.head
        self.head = remove.next
        self.size -= 1
        return remove.value
