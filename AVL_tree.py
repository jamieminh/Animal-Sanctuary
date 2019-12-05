class NodeAnimal:
    def __init__(self, animal):
        self.animal = animal
        self.key = animal.san_id
        self.left = None
        self.right = None
        self.height = 1

class NodePerson:
    def __init__(self, person_name):
        self.key = person_name
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:

    def __init__(self):
        self.root = None

    # SEARCH for animal using id
    def search(self, key, obj_type=""):
        node = self.search_recur(self.root, key)

        if obj_type == "person":
            if node is not None:
                return node.key
            else:
                return "Person with name " + key + " does not exist in the database."

        else:
            if node is not None:
                return node.animal
            else:
                return '\nAnimal with ID ' + key + ' does not exist.'

    # INSERT an object
    def insert(self, obj, obj_type=""):
        if obj_type == "person":
            self.root = self.insert_recur(self.root, NodePerson(obj))
        else:
            self.root = self.insert_recur(self.root, NodeAnimal(obj))

    # DELETE an object by id
    def delete(self, key, obj_type):
        if obj_type == "person":
            person = self.search(key, "person")
            if "not exist" in person:
                print(person)
            else:
                self.delete_recur(self.root, key)
                print("Person with name " + key + " has been deleted.")
        else:
            animal = self.search(key)
            if type(animal) is str:
                print(animal)
            else:
                self.delete_recur(self.root, key)
                print("Animal with ID " + key + " has been deleted.")

    # IN-ORDER traversal: (left -> root -> right) (Ascending order of animals' id)
    def in_order(self, obj_type=""):
        if obj_type == "person":
            self.in_order_recur(self.root, "person")
        else:
            self.in_order_recur(self.root)

    # Recursive method to search for id
    def search_recur(self, curr_root, key):
        # Case 1: if root is None, or id is at root
        if (curr_root is None) or (curr_root.key == key):
            return curr_root
        # Case 2: if id is greater than root's id
        if key > curr_root.key:
            return self.search_recur(curr_root.right, key)
        # Case 3: if id is smaller than root's id
        return self.search_recur(curr_root.left, key)

    # Recursive method to insert a node and balance the tree
    def insert_recur(self, curr_root, node):
        # insert in the right position
        if curr_root is None:
            return node
        elif node.key > curr_root.key:    # if value to be insert larger than value at root node, go right
            curr_root.right = self.insert_recur(curr_root.right, node)
        else:                   # if value to be insert smaller than value at root node, go left
            curr_root.left = self.insert_recur(curr_root.left, node)

        # Update height of root node
        self.update_height(curr_root)

        # get the height difference
        diff = self.get_difference(curr_root)

        # Perform Rotation to balance the tree
        # There are 4 cases:
        # Case 1: Left left -> rotate right
        if (curr_root.left is not None) and (node.key < curr_root.left.key) and (diff > 1):
            return self.right_rotate(curr_root)

        # Case 2: Right Right -> rotate left
        if (curr_root.right is not None) and (node.key > curr_root.right.key) and (diff < -1):
            return self.left_rotate(curr_root)

        # Case 3: Left Right -> rotate left, then rotate right
        if (curr_root.left is not None) and (node.key > curr_root.left.key) and (diff > 1):
            curr_root.left = self.left_rotate(curr_root.left)
            return self.right_rotate(curr_root)

        # Case 4: Right Left -> rotate right, then rotate left
        if (curr_root.right is not None) and (node.key < curr_root.right.key) and (diff < -1):
            curr_root.right = self.right_rotate(curr_root.right)
            return self.left_rotate(curr_root)

        return curr_root

    # Recursive method to delete node and balance the tree
    def delete_recur(self, curr_root, key):
        # ## Do normal Binary Search Tree delete
        if curr_root is None:
            return curr_root
        # if the id to be deleted is smaller than the curr_root's id => go left
        elif key < curr_root.key:
            curr_root.left = self.delete_recur(curr_root.left, key)
        # if the id to be deleted is greater than the curr_root's id => go right
        elif key > curr_root.key:
            curr_root.right = self.delete_recur(curr_root.right, key)
        # if none of the above cases is met, it means we have found our node
        else:
            # Node with only 1 child or no child
            if curr_root.right is None:
                temp = curr_root.left
                return temp
            elif curr_root.left is None:
                temp = curr_root.right
                return temp

            # Node with 2 children: successor is the smallest left in the right subtree
            temp = self.find_successor(curr_root.right)
            # assign the successor's id to the to-be-deleted node
            curr_root.key = temp.key
            # Delete the successor
            curr_root.right = self.delete_recur(curr_root.right, temp.key)

        if curr_root is None:
            return curr_root

        # ## Update height of ancestor node
        self.update_height(curr_root)

        # ### Get the height difference
        diff = self.get_difference(curr_root)

        # ### check for balance and rotate if necessary
        # Case 1: Right Right -> rotate left
        if (diff < -1) and (self.get_difference(curr_root.right) <= 0):
            return self.left_rotate(curr_root)

        # Case 2: Left Left -> rotate right
        if (diff > 1) and (self.get_difference(curr_root.left) >= 0):
            return self.right_rotate(curr_root)

        # Case 3: Right Left -> Rotate Right, then rotate Left
        if (diff < -1) and (self.get_difference(curr_root.right) > 0):
            curr_root.right = self.right_rotate(curr_root.right)
            return self.left_rotate(curr_root)

        # Case 4: Left Right -> rotate Left, then rotate Right
        if (diff > 1) and (self.get_difference(curr_root.left) < 0):
            curr_root.left = self.left_rotate(curr_root.left)
            return self.right_rotate(curr_root)

        return curr_root

    # Recursive method to in-order traverse the tree (left -> root -> right) (Ascending order of object's key)
    def in_order_recur(self, node, obj_type=""):
        if node is None:
            return

        if obj_type == "person":
            self.in_order_recur(node.left, "person")
            print(node.key, end="\n")
            self.in_order_recur(node.right, "person")
        else:
            self.in_order_recur(node.left)
            print(node.animal, end="\n")
            self.in_order_recur(node.right)

    # Find the logical successor: the leftmost leaf of the node's subtree
    def find_successor(self, node):
        curr = node
        # find the leftmost node
        while curr.left is not None:
            curr = curr.left
        return curr

    # Left Rotation around a node
    def left_rotate(self, node):
        R = node.right          # right branch of the node

        # rotation
        node.right = R.left     # right of node is now left of R :
        R.left = node           # left of R now points to node:

        # update height of nodes
        self.update_height(node)
        self.update_height(R)

        return R

    # Right Rotation around a node
    def right_rotate(self, node):
        L = node.left              # left branch of node

        # rotation
        node.left = L.right        # left of node is now right of 'L' : N.left = B3
        L.right = node             # right of 'L' now points to node: L.right = N

        # update height of nodes:
        self.update_height(node)
        self.update_height(L)

        return L

    # return height of a node
    def get_height(self, node):
        return node.height if (node is not None) else 0

    # Update height of a node
    def update_height(self, node):
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

    # returns height different of left and right branch of a mode
    def get_difference(self, node):
        return (self.get_height(node.left) - self.get_height(node.right)) if (node is not None) else 0





