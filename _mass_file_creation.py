import json
import os

def input_command():
    global command
    try:
        command = int(input())
        if command < 0 or command > 3:
            print("Input not in accepted range.")
            input_command()
    except:
        print("Invalid input. Please enter an integer.")
        input_command()

def should_skip(line):
    return line.startswith("#") or line.strip() == ""

# Pulls all items that should be decorated with icons into a list
def get_base_items():
    base_item_list = []
    with open("./_base_items.txt", "r") as item_list:
        for item in item_list:
            if should_skip(item):
                continue
            item_namespace = item.split(":")[0]
            item_name = item.split(":")[1].rstrip()
            base_item = [item_namespace, item_name]
            create_base_item_paths(base_item)
            base_item_list.append(base_item)
    return base_item_list

def create_base_item_paths(base_item):
    if not os.path.exists(f"./assets/{base_item[0]}/models/item/{base_item[1]}"):
        os.makedirs(f"./assets/{base_item[0]}/models/item/{base_item[1]}")
    if not os.path.exists(f"./assets/minecraft/optifine/cit/{base_item[0]}/{base_item[1]}"):
        os.makedirs(f"./assets/minecraft/optifine/cit/{base_item[0]}/{base_item[1]}")

def extract_enchant_info(line):
    details = line.split()
    namespace = details[0]
    enchant = details[1]
    level = details[2].rstrip()
    try:
        weight = details[3].rstrip()
    except IndexError:
        weight = None
    return namespace, enchant, level, weight

# CIT files at:
# /assets/minecraft/optifine/cit/<item_namespace>/<item_name>/<enchant_namespace>_<enchant_name>[_super].json
def create_cit_files(base_item, enchant_name, enchant_namespace, level, model_name_suffix, weight):
    model_file = f"{enchant_namespace}_{enchant_name}{model_name_suffix}"
    with open(f"./assets/minecraft/optifine/cit/{base_item[0]}/{base_item[1]}/{model_file}.properties", "w") as cit_file:
        cit_file.write("type=item\n")
        cit_file.write(f"items={base_item[0]}:{base_item[1]}\n")
        cit_file.write(f"enchantments={enchant_namespace}:{enchant_name}\n")
        cit_file.write(f"enchantmentLevels={level}\n")
        cit_file.write(f"model={base_item[0]}:item/{base_item[1]}/{model_file}\n")
        if weight:
            cit_file.write(f"weight={weight}\n")

# item model file at:
# /assets/<item_namespace>/models/item/<item_name>/<enchant_namespace>_<enchant_name>.json       
def create_model_files(base_item, enchant_namespace, enchant_name):
    with open(f"./assets/{base_item[0]}/models/item/{base_item[1]}/{enchant_namespace}_{enchant_name}.json", "w") as output_model:
        model = {"parent": f"{base_item[0]}:item/{base_item[1]}", "textures": {"layer1": f"{enchant_namespace}:item/{enchant_name}"}}
        json.dump(model, output_model, indent=4)

# item model file at:
# /assets/<item_namespace>/models/item/<item_name>/<enchant_namespace>_<enchant_name>_super.json
def create_model_super_files(base_item, enchant_namespace, enchant_name):
    with open(f"./assets/{base_item[0]}/models/item/{base_item[1]}/{enchant_namespace}_{enchant_name}_super.json", "w") as output_model:
        model = {"parent": f"{base_item[0]}:item/{base_item[1]}", "textures": {"layer1": "minecraft:item/super_level_indicator", "layer2": f"{enchant_namespace}:item/{enchant_name}"}}
        json.dump(model, output_model, indent=4)

def run_command():
    if command == 0:
        return
    base_item_list = get_base_items()
    with open("./_enchantments.txt", "r") as enchant_list:
        for line in enchant_list:
            # skip these that shouldn't be created
            if should_skip(line):
                continue
            enchant_namespace, enchant_name, level, weight = extract_enchant_info(line)
            for base_item in base_item_list:
                if (command >> 0) & 1:
                    # CIT files for vanilla max levels
                    create_cit_files(base_item, enchant_name, enchant_namespace, level, "", weight)
                    # CIT files for levels higher than vanilla obtainable
                    create_cit_files(base_item, enchant_name, enchant_namespace, f"{int(level) + 1}-", "_super", weight)
                # similar things here, for model files
                if (command >> 1) & 1:
                    create_model_files(base_item, enchant_namespace, enchant_name)
                    create_model_super_files(base_item, enchant_namespace, enchant_name)

if __name__ == "__main__":
    command = -1
    print("Input a number for the following processes:\n\n" \
          "0 - Exit the programme\n" \
          "1 - Create CIT files\n" \
          "2 - Create Model files\n\n" \
          "Input a sum of numbers will run them at once.")
    input_command()
    run_command()
    input("Done! Press any key to exit...")