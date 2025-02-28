import re

def split_sections(md):
    match = re.search(r"(?s)(\.DATA.*?)?(?=(\.LOGIC))(\.LOGIC.*)", md)

    if not match:
        return None, None

    data_section = match.group(1).strip() if match.group(1) else None
    logic_section = match.group(3).strip()

    return data_section, logic_section

def validateDataSection(ds):
    defined_memories = {}
    if ds:
        lines = ds.split("\n")[1:]
        for line in lines:
            line = line.strip()
            if line:
                match = re.match(r"^(STACK|QUEUE|TAPE|2D_TAPE)\s+(\w+)$", line)
                if not match:
                    return defined_memories, False, f"Invalid .DATA definition: '{line}'"
                mem_type, mem_name = match.groups()
                defined_memories[mem_name] = mem_type

    return defined_memories, True, "Valid .DATA section"

def validateLogicSection(ls, defined_memories):
    logic = {}
    normal_commands = {"SCAN", "PRINT", "SCAN RIGHT", "SCAN LEFT", "READ", "WRITE"}
    tape_commands = {"RIGHT", "LEFT", "UP", "DOWN"}

    logic_lines = ls.split("\n")[1:] 
    normal_pattern = re.compile(
        r"^(\w+)]\s+(SCAN|PRINT|SCAN RIGHT|SCAN LEFT|READ|WRITE)(?:\((\w+)\))?\s*((?:\([^,]+,\s*[^)]+\),?\s*)+)$"
    )
    tape_pattern = re.compile(
        r"^(\w+)]\s+(RIGHT|LEFT|UP|DOWN)\((\w+)\)\s*((?:\([^/]+/[^,]+,\s*[^)]+\),?\s*)+)$"
    )

    # first pass, extract all state names
    for line in logic_lines:
        line = line.strip()
        if line:
            state_match = re.match(r"^(\w+)]", line)
            if state_match:
                state_name = state_match.group(1)
                logic[state_name] = {"command": None, "memory": None, "transitions": []}

    # second pass, validate and extract commands and transitions
    for line in logic_lines:
        line = line.strip()
        if not line:
            continue

        normal_match = normal_pattern.match(line)
        tape_match = tape_pattern.match(line)

        if normal_match:
            state = normal_match.group(1)
            command = normal_match.group(2).strip()
            memory_name = normal_match.group(3)
            transitions_raw = normal_match.group(4)

            if command not in normal_commands:
                return logic, False, f"Invalid command '{command}' in .LOGIC section"

            if memory_name and memory_name not in defined_memories:
                return logic, False, f"Memory structure '{memory_name}' used in '{command}' is not defined in .DATA"

            transitions = re.findall(r"\(([^,]+),\s*([^)]+)\)", transitions_raw)
            logic[state] = {
                "command": command,
                "memory": memory_name,
                "transitions": transitions
            }

        elif tape_match:
            state = tape_match.group(1)
            command = tape_match.group(2).strip()
            memory_name = tape_match.group(3).strip()
            transitions_raw = tape_match.group(4)

            if command not in tape_commands:
                return logic, False, f"Invalid command '{command}' in .LOGIC section"

            if memory_name not in defined_memories:
                return logic, False, f"Memory structure '{memory_name}' used in '{command}' is not defined in .DATA"

            if defined_memories[memory_name] != "TAPE" and defined_memories[memory_name] != "2D_TAPE":
                return logic, False, f"Memory '{memory_name}' cannot be used with movement command '{command}'"
            
            if defined_memories[memory_name] == "TAPE" and command in {"UP", "DOWN"}:
                return logic, False, f"Memory '{memory_name}' cannot be used with movement command '{command}'"

            transitions = re.findall(r"\(([^/]+)/([^,]+),\s*([^)]+)\)", transitions_raw)
            logic[state] = {
                "command": command,
                "memory": memory_name,
                "transitions": [(s1, s2, dest) for s1, s2, dest in transitions]
            }

        else:
            return logic, False, f"Invalid .LOGIC definition: '{line}'"

    # final pass to check if all destination states are defined
    for state, data in logic.items():
        for transition in data["transitions"]:
            dest_state = transition[-1]
            if dest_state not in logic and dest_state not in {"accept", "reject"}:
                return logic, False, f"State '{dest_state}' used in transitions is not defined in .LOGIC"

    return logic, True, "Valid .LOGIC section"

def extractMachineDefinition(md):
    memory = {}
    logic = {}
    md = md.strip()

    if not re.search(r'\.LOGIC', md):
        return memory, logic, False, "Missing .LOGIC section"

    data_section, logic_section = split_sections(md)

    if not logic_section or logic_section.strip() == ".LOGIC":
        return memory, logic, False, "The .LOGIC section cannot be empty"
    
    memory, valid, error = validateDataSection(data_section)
    if not valid:
        return memory, logic, False, error

    logic, valid, error = validateLogicSection(logic_section, memory)
    if not valid:
        return memory, logic, False, error

    return memory, logic, True, "Valid machine definition"