# create weapon equip screen
class Shop:
    class Improvements:
        """
        All upgrades and costs
        """
        bigger_bullets = {k: 10 * k for k in range(1, 12)}  # weapon cost * level
        faster_bullets = {k: 15 * k for k in range(1, 12)}
        player_speed_increase = {}
        player_hp_increase = {}

    class Weapons:
        """
        All weapons and costs
        """
        expand_shot = {1: 50000}
        stalker_missile = {1: 125000}
        ray_of_light = {1: 250000}

    # black_hole = {1: 999999999}

    class PowerUps:
        """
        All powerups and costs
        """
        shield = {1: 1000, 2: 2500, 3: 5000}  # level 1: 150hp 2: 300hp 3: 500hp (3 shields allowed per round)
        invinsibility = {1: 2500, 2: 5000,
                         3: 7500}  # level 1: 3secs 2: 7secs 3: 12secs (1 invinsibility allowed per round)
        nuke = {1: 12500}  # destroys all enemies on the screen (1 nuke allowed per round)

    @staticmethod
    def retrieve_cost(id, level):
        return id[level]

    @staticmethod
    def Purchase(id):
        pass


attribute_list = ["player_attributes"]
weapon_list = ["single_shot", "expand_shot", "stalker_missile", "ray_of_light"]  # names of all available weapons
upgrade_list = ["bigger_bullets", "faster_bullets", "player_speed_increase", "player_hp_increase"]  # names of all available upgrades
powerup_list = ["shield", "invinsibility", "nuke"]  # names of all available powerups

current_upgrades = {attribute_list[0]: {upgrade_list[2]: 10, upgrade_list[3]: 10},
                    weapon_list[0]: {upgrade_list[0]: 0, upgrade_list[1]: 0},
                    weapon_list[1]: {upgrade_list[0]: 10, upgrade_list[1]: 10},
                    weapon_list[2]: {upgrade_list[0]: 10, upgrade_list[1]: 10},
                    weapon_list[3]: {upgrade_list[0]: 10, upgrade_list[1]: 10},
                    }  # the current upgrades of all players weapons (retreieve from json file)

inventory_dict = {weapon_list[0]: "owned", weapon_list[1]: "unowned", weapon_list[2]: "unowned",
                  weapon_list[3]: "unowned", powerup_list[0]: {"amount": {1: 0, 2: 0, 3: 0}},
                  powerup_list[1]: {"amount": {1: 0, 2: 0, 3: 0}}, powerup_list[2]: {"amount": {1: 0}}
                  }  # the current inventory of player (checks whether a weapon is owned and checks the level of the upgrades and amount of upgrades) (load from json)

current_loadout = {
    "attribute_loadout":
        {"attribute_level": {upgrade_list[2]: current_upgrades[attribute_list[0]][upgrade_list[2]], upgrade_list[3]: current_upgrades[attribute_list[0]][upgrade_list[3]]}},
    "weapon_loadout":
        {"current_weapon": weapon_list[3], "weapon_level": None},
    "powerup_loadout":
        {"current_powerups": {powerup_list[0]: inventory_dict[powerup_list[0]],
                         powerup_list[1]: inventory_dict[powerup_list[1]],
                         powerup_list[2]: inventory_dict[powerup_list[2]]}}
                   }   # current loadout for player (load from json)

current_loadout["weapon_loadout"]["weapon_level"] = current_upgrades[
    current_loadout["weapon_loadout"]["current_weapon"]]  # assign current_level

#print(current_loadout)

upgrades_dict = {upgrade_list[0]: Shop.retrieve_cost(Shop.Improvements.bigger_bullets,
                                                     current_loadout["weapon_loadout"]["weapon_level"][upgrade_list[0]] + 1),
                 upgrade_list[1]: Shop.retrieve_cost(Shop.Improvements.faster_bullets,
                                                     current_loadout["weapon_loadout"]["weapon_level"][upgrade_list[1]] + 1)}  # the cost of the next level upgrade (implement boundaries)

#print(upgrades_dict["faster_bullets"])
