import re

def split_sections(md):
    data_section = None
    logic_section = None

    parts = md.split('.LOGIC', 1)
    if len(parts) == 2:
        logic_section = '.LOGIC\n' + parts[1].strip()

        data_index = parts[0].find('.DATA')
        if data_index != -1:
            data_section = parts[0][data_index:].strip()

    return data_section, logic_section

def validateDataSection(ds):
    memory = {}
    valid_structures = {"STACK", "QUEUE", "TAPE", "2D_TAPE"}

    if ds is not None:
        lines = ds.split("\n")[1:]
        for line in lines:
            line = line.strip()
            if line:
                parts = line.split()
                
                if len(parts) != 2:
                    return memory, False, f"Invalid .DATA definition: '{line}'"
                
                mem_type, mem_name = parts
                if mem_type not in valid_structures:
                    return memory, False, f"Invalid memory type: '{mem_type}'"

                if mem_name in memory:
                    return memory, False, f"Duplicate memory name detected: '{mem_name}'"

                memory[mem_name] = mem_type

    return memory, True, "Valid .DATA section"

def validateLogicSection(ls):
    logic = {}
    normal_commands = {"SCAN", "PRINT", "SCAN RIGHT", "SCAN LEFT", "READ", "WRITE"}
    tape_commands = {"RIGHT", "LEFT", "UP", "DOWN"}
    lines = ls.split("\n")[1:] 

    # extract all state names and initialize logic dictionary
    for line in lines:
        line = line.strip()
        if line:
            if "]" in line:
                state = line.split("]")[0].strip()
                if state in logic:
                    return logic, False, "Duplicate state name detected: " + state
                logic[state] = {"command": None, "memory": None, "transitions": []}

    # validate commands and extract transitions
    for line in lines:
        line = line.strip()
        if not line:
            continue # skip empty lines

        parts = line.split("]")
        if len(parts) != 2:
            return logic, False, f"Invalid .LOGIC definition: '{line}'"

        state = parts[0].strip()
        command = parts[1].strip().split("(")[0].strip()
        mem_symbol = None
        index = parts[1].find("(")
        index_end = parts[1].find(")")

        if command in normal_commands:
            if command not in ["SCAN", "PRINT", "SCAN RIGHT", "SCAN LEFT"]:
                mem_symbol = parts[1][index + 1 : index_end].strip() if index != -1 and index_end != -1 else None
                remainder = parts[1][index_end + 1 :].strip() if index_end != -1 else ""
            else:
                remainder = parts[1][index:].strip() if index != -1 else ""
            
            transitions = []
            value = ""

            for char in remainder:
                if char == "(":
                    value = ""
                elif char == ")":
                    transitions.append(tuple(map(str.strip, value.split(","))))
                else:
                    value += char

            logic[state] = {"command": command, "memory": mem_symbol, "transitions": transitions}

        elif command in tape_commands:
            mem_symbol = parts[1][index + 1 : index_end].strip() if index != -1 and index_end != -1 else None
            remainder = parts[1][index_end + 1 :].strip() if index_end != -1 else ""

            transitions = []
            value = ""

            for char in remainder:
                if char == "(":
                    value = ""
                elif char == ")":
                    items = value.strip().split(",")
                    if len(items) == 2:  
                        left, right = map(str.strip, items[0].split("/"))
                        transitions.append((left, right, items[1].strip()))
                else:
                    value += char
            
            logic[state] = {"command": command, "memory": mem_symbol, "transitions": transitions}

        else:
            return logic, False, f"Invalid .LOGIC definition: '{line}'"

    return logic, True, "Valid .LOGIC section"

def extractMachineDefinition(md):
    memory_dict = {}
    logic_dict = {}

    # split the machine definition into data and logic sections
    data_section, logic_section = split_sections(md)

    # error handling for missing or empty .LOGIC section
    if logic_section is None:
        return memory_dict, logic_dict, False, "Missing .LOGIC section"
    if logic_section.strip() == ".LOGIC":
        return memory_dict, logic_dict, False, "The .LOGIC section cannot be empty"
    
    # validate data section and store in dictionary
    memory_dict, valid, error = validateDataSection(data_section)
    if not valid:
        return memory_dict, logic_dict, False, error

    # validate logic section and store in dictionary
    logic_dict, valid, error = validateLogicSection(logic_section)
    if not valid:
        return memory_dict, logic_dict, False, error

    return memory_dict, logic_dict, True, "Valid machine definition"

def format_memory(memory_structures):
    memory_structures = re.sub(r'(\b\w+)(:)', r'<b>\1</b>\2', memory_structures)
    memory_structures = memory_structures.replace("\n", "<br>")
    memory_structures = re.sub(r'style="([^"]*?)<b>(.*?)</b>([^"]*?)"', r'style="\1\2\3"', memory_structures)
    memory_structures = re.sub(r'(<span[^>]*?style="[^"]*?)<b>(.*?)</b>([^"]*?">)', r'\1\2\3', memory_structures)

    return memory_structures

