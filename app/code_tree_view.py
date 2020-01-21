import requests
class GetTree():

    # Get the number of spaces at the beginning of each line in the code 
    def print_code(self,url):
        response = requests.get(url)
        f = response.content
        return f

    
    def space_number(self,elem):
        index = 0
        while index < len(elem):
            if elem[index] != ' ':
                return(len(elem[0:index]))
                break
            index += 1

    def read_code(self,url):
        response = requests.get(url)
        f = response.content.decode()
        code = f.split('\n')
        code_in_str_list = []
        for elem in code:
            if elem != '':
                code_in_str_list.append(elem)
        return code_in_str_list
        print (code_in_str_list)


    # Get the name and the level of each function or class in the code
    def get_level_name(self,code_in_str_list):
        function_name0 = []
        function_name = []
        function_level = []
        for elem in code_in_str_list:
            index = 0
            while index < len(elem):
                symbol = elem[index]
                if symbol == ' ':
                    space = index
                elif symbol == '(':
                    if elem[0] != ' ':
                        function_name0.append(elem[space + 1:index])
                        function_level.append(0)
                    else:
                        if elem[space +1].islower():
                            function_name0.append(elem[space + 1:index])
                            function_level.append(int(GetTree().space_number(elem) / 4))
                index += 1

        for name in function_name0:
            if 'self' in name:
                function_name.append(name[5:])
            else:
                function_name.append(name)

        return function_level, function_name

    def get_class(self,function_name):
        function_class=[]
        for elem in function_name:
            if '.' in elem:
                function_class.append('0')
            else:
                function_class.append('1')
        return function_class


    # Put functions and classes in the form of tree using dictionary
    def layout_code(self,level_list, function_list,class_list):
        
        # Treat each function or class as a member
        members = []
        # Create a basic dictionary (without the value of 'children') for each member 
        for i in range(len(level_list)):
            members.append({
                'name': function_list[i],
                'level': level_list[i],
                'thisclass': class_list[i],
                'index': i,
                'children': []
            })

        # Group the members by their levels in the code
        lst_levels_indices = []
        for i in range(max(level_list) + 1):
            lst_levels_indices.append(
                [j for j in range(len(level_list)) if level_list[j] == i])

        # Assign 'children' to each member from the bottom up
        for i in reversed(range(len(lst_levels_indices))):
            if i != 0:
                level_indices = lst_levels_indices[i]

                for index in level_indices:
                    
                    for k in reversed(range(index)):
                        if k in lst_levels_indices[i - 1]:

                            members[k]['children'].append(members[index])
                            break
        # Return the top-most member as the structure of whole family
        return members[0]

# tree = GetTree()
# url = 'https://raw.githubusercontent.com/ZiyeHan/pseudo-py-codes/master/pseudo-py-1.py'
# code_in_str_list = tree.read_code(url)
# level_list, function_list = tree.get_level_name(code_in_str_list)
# family = tree.layout_code(level_list, function_list)
# print(family)
