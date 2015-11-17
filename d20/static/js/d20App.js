var app = angular.module('d20', ['ngDialog', 'siyfion.sfTypeahead'], function ($interpolateProvider, $locationProvider) {
    $interpolateProvider.startSymbol("{[{");
    $interpolateProvider.endSymbol("}]}");
    $locationProvider.html5Mode(true);
});

app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

app.config(['ngDialogProvider', function (ngDialogProvider) {
	ngDialogProvider.setDefaults({
		className: 'ngdialog-theme-default',
		plain: false,
		showClose: true,
		closeByDocument: true,
		closeByEscape: true,
	});
}]);

//Rolling function.
//Takes a number of dice to roll {num}
//What die to roll {die}, which is 20 for a d20, 8 for a d8, etc.
//A modifier to add to the total, if any.
//Returns an object with the individual results in an array, and the total.
var roll = function(num, die, mod){
	var results = [];
	var total = 0;
	if (num > 0){
		for(var i = 0; i < num; i++){
			var result = Math.floor((Math.random() * die) + 1);
			results.push(result);
			total += result;
		}
	}
	total += mod;
	var obj = {
		total: total,
		results: results,
		num: num,
		die: die,
		mod: mod
	};

	return obj;
};

app.controller('DiceController', function($scope, ngDialog){
	$scope.openPopup = function (id, name) {
		$scope.name = name;
		console.log("opening popup");
		ngDialog.open({
			template: '/popup',
			overlay: false,
			closeByEscape: false,
			scope: $scope,
			showClose: false,
		});
	};
});

app.controller('PopupController', function($scope, ngDialog){

});

app.service('characterService', function($http, $q){

	var api_url = "/api/";
	var weapon_api_url = "/api/weapons/";
	var weapon_create_url = weapon_api_url + "create";
	var spell_school_api_url = "/api/spellschool/";
	var spell_school_create_url = spell_school_api_url + "create";
	var spell_api_url = "/api/spell/";
	var spell_create_url = spell_api_url + "create";

	var skills_order = [
		["Acrobatics", "dex", "acro_skill"],
		["Appraise", "int", "appraise_skill"],
		["Bluff", "cha", "bluff_skill"],
		["Climb", "str", "climb_skill"],
		["Craft 1", "int", "craft1_skill", "craft1_name"],
		["Craft 2", "int", "craft2_skill", "craft2_name"],
		["Craft 3", "int", "craft3_skill", "craft3_name"],
		["Diplomacy", "cha", "diplomacy_skill"],
		["Disable Device", "dex", "disable_dev_skill"],
		["Disguise", "cha", "disguise_skill"],
		["Escape Artist", "dex", "escape_art_skill"],
		["Fly", "dex", "fly_skill"],
		["Handle Animal", "cha", "handle_animal_skill"],
		["Heal", "wis", "heal_skill"],
		["Intimidate", "cha", "intimidate_skill"],
		["Knowledge (Arcana)", "int", "arcana_skill"],
		["Knowledge (Dungeoneering)", "int", "dungeon_skill"],
		["Knowledge (Engineering)", "int", "engineering_skill"],
		["Knowledge (Geography)", "int", "geography_skill"],
		["Knowledge (History)", "int", "history_skill"],
		["Knowledge (Local)", "int", "local_skill"],
		["Knowledge (Nature)", "int", "nature_skill"],
		["Knowledge (Nobility)", "int", "nobility_skill"],
		["Knowledge (Planes)", "int", "planes_skill"],
		["Knowledge (Religion)", "int", "religion_skill"],
		["Linguistics", "int", "linguistics_skill"],
		["Perception", "wis", "perception_skill"],
		["Perform 1", "cha", "perform1_skill", "perform1_name"],
		["Perform 2", "cha", "perform2_skill", "perform2_name"],
		["Profession 1", "wis", "prof1_skill", "prof1_name"],
		["Profession 2", "wis", "prof2_skill", "prof2_name"],
		["Ride", "dex", "ride_skill"],
		["Sense Motive", "wis", "sense_motive_skill"],
		["Sleight of Hand", "dex", "sleight_skill"],
		["Spellcraft", "int", "spellcraft_skill"],
		["Stealth", "dex", "stealth_skill"],
		["Survival", "wis", "survival_skill"],
		["Swim", "str", "swim_skill"],
		["Use Magic Item", "cha", "use_magic_skill"]
	];

	var abilities_order = ["str", "dex", "con", "int", "wis", "cha"];

	var sizes = {
        '-8': 'Colossal',
        '-4': 'Gargantuan',
        '-2': 'Huge',
        '-1': 'Large',
        '0': 'Medium',
        '1': 'Small',
        '2': 'Tiny',
        '4': 'Diminutive',
        '8': 'Fine'
    };

    var save_names = [ 
		{name: "Fortitude", short: "fort", mod: "con"},
		{name: "Reflex", short: "reflex", mod: "dex"},
		{name: "Will", short: "will", mod: "wis"},
	];

	var genders = {
		"M": "Male",
		"F": "Female",
		"O": "Other"
	};

	var spell_mods_options = {
		"int": "Intelligence", 
		"wis": "Wisdom",
		"cha": "Charisma"
	};

	var c = {};

	var _set_mod= function(abil, scores){
		var abil_score = parseInt(scores[0]);
		var abil_temp = parseInt(scores[1]);
		var mod_value = _calculate_mod(abil_score + abil_temp);
		c[abil] = {
			"score": abil_score,
			"mod": mod_value,
			"temp": abil_temp,
		};
	};

	var _calculate_mod = function(score){
		return Math.floor((parseInt(score) - 10) / 2);
	};

	var _set_skill = function(name, abil, data, extra){	
		var class_skill = false;
		if(data[0] == "1"){
			class_skill = true;
		}
		var s = c[abil].mod;
		var r = parseInt(data[1]);
		var m = parseInt(data[2]);
		var total = s + r + m;
		if(class_skill && r > 0){
			total += 3;
		}
		var new_obj = {
			name: name,
			abil: abil,
			abil_mod: s,
			total: total,
			c_skill: class_skill,
			ranks: r,
			misc: m,
		};
		if(extra !== undefined){
			new_obj.extra = extra;
		}
		c.skills.push(new_obj);
		c.total_ranks += r;
	};

	var _cacluate_AC_totals = function(){
		var total = 10;
		total += c.ac.armor + c.ac.shield + c.ac.nat + c.ac.deflect + c.ac.misc;
		total += c.dex.mod + c.size_mod;
		c.ac.total = total;
		var touch = total - c.ac.armor - c.ac.shield - c.ac.nat;
		var flat = total - c.dex.mod;
		c.ac.touch = touch;
		c.ac.flat = flat;
	};

	var _calculate_save = function(save){
		var total = 0;
		total += c[save].base + c[save].magic + c[save].misc + c[save].temp;
		total += c[c[save].mod_name].mod;
		c[save].total = total;	
	};

	var _calculate_CMs = function(){
		var littles = ["Tiny", "Diminutive", "Fine"];
		if(littles.indexOf(c.size) > -1){
			//CMB for tiny or smaller = BAB + Dex - Size Mod
			c.cmb = c.base_attack + c.dex.mod - c.size_mod;
			c.cmb_mod = c.dex.mod;
		} else {
			//CMB = BAB + Str - Size Mod
			c.cmb = c.base_attack + c.str.mod - c.size_mod;
			c.cmb_mod = c.str.mod;
		}

		//CMD = BAB + Str + Dex - Size Mod + 10
		c.cmd = 10 + c.base_attack + c.str.mod + c.dex.mod - c.size_mod;
	};

	var _calculate_hp_percent = function(){
		if(c.hp_percent === undefined){
			c.hp_percent = 0;
		}
		if(c.hp > 0){
			c.hp_percent = ((c.current_hp / c.hp) * 100).toFixed(2);
		}
		var percent = c.hp_percent;
		if(percent >= 50){
			$("#hp-progress").removeClass("progress-bar-warning progress-bar-danger").addClass("progress-bar-success");
		} else if (percent < 50 && percent >= 25){
			$("#hp-progress").removeClass("progress-bar-success progress-bar-danger").addClass("progress-bar-warning");
		} else {
			$("#hp-progress").removeClass("progress-bar-warning progress-bar-success").addClass("progress-bar-danger");
		}
	};

	var _getWeaponData = function(weapon_url){
		$http.get(weapon_url).then(function(response){
			var data = response.data;
			c.weapons.push(data);
			return data;
		});
	};

	var _getSpellSchool = function(school_url){
		$http.get(school_url).then(function(response){
			var data = response.data;
			data.known_spells = data.known_spells.split(",");
			data.spells_per_day = data.spells_per_day.split(",");
			data.bonus_spells = data.bonus_spells.split(",");
			data.spell_mod_full = spell_mods_options[data.spell_mod];

			var spells = data.spells;
			var spell_list = [[], [], [], [], [], [], [], [], [], []];
			for(var i in spells){
				var level = spells[i].spell_level;
				spell_list[level].push(spells[i]);
			}
			data.spell_list = spell_list;
			c.spell_schools.push(data);
			return data;
		});
	};

	var _setdata = function(data){
		//Set basic data
		c.name = data.name;
		c.player = data.player;
		c.id = data.id;

		c.size_mod = parseInt(data.size);
		c.alignment = data.alignment;
		c.char_class = data.char_class;
		c.level = data.level;
		c.deity = data.deity;
		c.homeland = data.homeland;
		c.race = data.race;
		c.size = sizes[String(data.size)];
		c.gender = genders[data.gender];
		c.age = data.age;
		c.height = data.height;
		c.weight = data.weight;
		c.hair = data.hair;
		c.eyes = data.eyes;
		c.languages = data.languages;
		c.desc = data.description;
		c.notes = data.notes;
		
		var xp_values = data.xp.split(",");
		c.xp = parseInt(xp_values[0]) || 0;
		c.next_level = parseInt(xp_values[1]) || 0;

		//Set metadata
		c.meta = {
			"public": data.is_public,
			"created": data.created,
			"updated": data.last_updated,
			"type": data.sheet_type
		};

		//Set ability scores and mods
		for(var i in abilities_order){
			var abil = abilities_order[i];
			var abil_name = abil + "_score";
			var scores = data[abil_name].split(",");
			_set_mod(abil, scores);
		}

		//Set skill totals and mods
		c.skills = [];
		c.total_ranks = 0;
		for(var j in skills_order){
			var skill = skills_order[j];
			var skill_name = skill[0];
			var skill_abil = skill[1];
			var skill_model = skill[2];
			var skill_extra = skill[3];
			var skill_data = data[skill_model].split(",");
			var skill_extra_data;
			if(skill_extra !== undefined ){
				skill_extra_data = data[skill_extra];
			}
			_set_skill(skill_name, skill_abil, skill_data, skill_extra_data);
		}

		c.hp = data.hp_total;
		c.current_hp = data.current_hp;
		_calculate_hp_percent();
		c.init_mod = parseInt(data.init_mod) || 0;
		c.base_attack = data.base_attack;

		//Speeds
		var speed_vals = data.speed.split(",");
		c.speeds = {
			base: parseInt(speed_vals[0]),
			armor: parseInt(speed_vals[1]),
			fly: parseInt(speed_vals[2]),
			swim: parseInt(speed_vals[3]),
			climb: parseInt(speed_vals[4]),
			burrow: parseInt(speed_vals[5])
		};

		//AC stuff
		//5 integers separated by commas in the format of:
    	//'armor_bonus,shield_bonus,nat_armor,deflection_mod,misc_mod'
		var ac_stats = data.ac_mods.split(",");
		c.ac = {
			armor: parseInt(ac_stats[0]),
			shield: parseInt(ac_stats[1]),
			nat: parseInt(ac_stats[2]),
			deflect: parseInt(ac_stats[3]),
			misc: parseInt(ac_stats[4]),
		};
		_cacluate_AC_totals();

		// Saves
		//stats are in the format of:
    	//[base_save, magic_mod, misc_mod, temp_mod]
		for(var k in save_names){
			var save = save_names[k];
			var save_data = data[save.short + "_save"].split(",");
			var obj = {
				name: save.name,
				mod_name: save.mod,
				base: parseInt(save_data[0]),
				magic: parseInt(save_data[1]),
				misc: parseInt(save_data[2]),
				temp: parseInt(save_data[3]),
			};
			c[save.short] = obj;
			_calculate_save(save.short);
		}

		c.dr = data.damage_reduction;
		c.spell_resist = data.spell_resist;

		//Calculate CMD and CMB
		_calculate_CMs();


		//Weapons
		c.weapon_slugs = data.weapons;
		c.weapons = [];
		for(var l in c.weapon_slugs){
			var slug = c.weapon_slugs[l];
			var url = weapon_api_url + slug;
			_getWeaponData(url);
		}
		c.new_weapon = {character: c.id};

		//Feats
		c.feats = data.feats;
		c.custom_feats = [];
		if((data.custom_feats !== undefined) && (data.custom_feats !== "")){
			c.custom_feats = data.custom_feats.split(",");
		}

		//Money
		var money_data = data.money.split(",");
		c.money = {
			platinum: parseInt(money_data[0]),
			gold: parseInt(money_data[1]),
			silver: parseInt(money_data[2]),
			copper: parseInt(money_data[3])
		};
		c.loot = data.loot;
		
		//Spells
		c.spell_schools_slugs = data.spell_schools;
		c.spell_schools = [];
		for(var m in c.spell_schools_slugs){
			var spell_slug = c.spell_schools_slugs[m];
			var spell_school_url = spell_school_api_url + spell_slug;
			_getSpellSchool(spell_school_url);
		}

	};

	var updateSkillTotals = function(){
		c.total_ranks = 0;
		for (var i in c.skills){
			var obj = c.skills[i];
			var abil = obj.abil;
			var r = obj.ranks;
			var m = obj.misc;
			var new_total = c[abil].mod + r + m;
			if(obj.c_skill && r > 0){
				new_total += 3;
			}
			obj.total = new_total;
			obj.abil_mod = c[abil].mod;
			c.total_ranks += r;
		}
	};

	var updateAc = function(){
		_cacluate_AC_totals();
	};

	var updateSaves = function(){
		for(var i in save_names){
			var save_name = save_names[i].short;
			_calculate_save(save_name);
		}
	};

	var updateCMs = function(){
		_calculate_CMs();
	};

	this.getCharacter = function(url){
		api_url = url;
		$http.get(url).then(function(response){
			var data = response.data;
			_setdata(data);
			return data;
		});
		return c;
	};

	this.get_abil_order = function(){
		return abilities_order;
	};

	this.updateAbil = function(abil, new_values){
		c[abil].score = new_values.score;
		c[abil].temp = new_values.temp;
		c[abil].mod = _calculate_mod(c[abil].score + c[abil].temp);
		updateSkillTotals();
		updateAc();
		updateSaves();
		updateCMs();
	};

	this.updateSkills = function(){
		updateSkillTotals();
	};

	this.updateSaves = function(){
		updateSaves();
	};

	this.updateAC = function(){
		updateAc();
	};

	this.updateSizeMod = function(mod){
		c.size_mod = mod;
		updateAc();
		updateCMs();
	};

	this.updateBAB = function(){
		updateCMs();
	};

	this.addFeat = function(feat){
		if (feat !== ""){
			c.feats.push(feat);
		}
	};

	this.deleteFeat = function(feat){
		var index = -1;
		for(var i = 0, len = c.feats.length; i < len; i++) {
		    if (c.feats[i] === feat) {
		        index = i;
		        break;
		    }
		}
		if(index > -1){
			c.feats.splice(index, 1);
		}
	};

	this.addCustomFeat = function(feat){
		if (feat !== ""){
			c.custom_feats.push(feat);
		}
	};

	this.deleteCustomFeat = function(feat){
		var index = -1;
		for(var i = 0, len = c.custom_feats.length; i < len; i++) {
		    if (c.custom_feats[i] === feat) {
		        index = i;
		        break;
		    }
		}
		if(index > -1){
			c.custom_feats.splice(index, 1);
		}
	};

	this.addWeapon = function(){
		var weapon_obj = c.new_weapon;
		$http.post(weapon_create_url, weapon_obj).success(function(data, status, headers, config) {
			c.weapons.push(data);
		}).error(function(data, status, headers, config) {
			console.log("Create returned: " + status);
			console.log(data);
		});
		c.new_weapon = {character: c.id};
	};

	this.deleteWeapon = function(weapon){
		var weapon_url = weapon_api_url + weapon.slug;
		var index = -1;
		for(var i = 0, len = c.weapons.length; i < len; i++) {
		    if (c.weapons[i].slug === weapon.slug) {
		        index = i;
		        break;
		    }
		}
		if(index > -1){
			c.weapons.splice(index, 1);
		}
		$http.delete(weapon_url).success(function(data, status, headers, config) {
			console.log("Deleted weapon: " + weapon.slug);
		}).error(function(data, status, headers, config) {
			console.log("Delete returned: " + status);
			console.log(data);
		});

	};

	this.calculate_hp_percent = function(){
		_calculate_hp_percent();
	};

	this.updateSpellMod = function(school){
		school.spell_mod = school.spell_mod_full.toLowerCase().substring(0,3);
	};

	this.addSchool = function(school_name){
		var school_obj = {
			name: school_name,
			character: c.id
		};
		console.log(school_obj);
		$http.post(spell_school_create_url, school_obj).success(function(data, status, headers, config) {
			data.known_spells = data.known_spells.split(",");
			data.spells_per_day = data.spells_per_day.split(",");
			data.bonus_spells = data.bonus_spells.split(",");
			data.spell_mod_full = spell_mods_options[data.spell_mod];
			c.spell_schools.push(data);
		}).error(function(data, status, headers, config) {
			console.log("Create returned: " + status);
			console.log(data);
		});
	};

	this.deleteSchool = function(school){
		var school_url = spell_school_api_url + school.slug;
		var index = -1;
		for(var i = 0, len = c.spell_schools.length; i < len; i++) {
		    if (c.spell_schools[i].slug === school.slug) {
		        index = i;
		        break;
		    }
		}
		if(index > -1){
			c.spell_schools.splice(index, 1);
		}
		$http.delete(school_url).success(function(data, status, headers, config) {
			console.log("Deleted school: " + school.slug);
		}).error(function(data, status, headers, config) {
			console.log("Delete returned: " + status);
			console.log(data);
		});
	};

	this.addSpell = function(spell_obj, school){
		console.log(spell_obj);
		$http.post(spell_create_url, spell_obj).success(function(data, status, headers, config) {
			console.log(data);
			console.log(school);
			school.spell_list[spell_obj.spell_level].push(data);
		}).error(function(data, status, headers, config) {
			console.log("Create returned: " + status);
			console.log(data);
		});

	};

	var updateObject = function(url, data){
		$http.patch(url, data).success(function(data, status, headers, config) {
			console.log("Saved!");
		}).error(function(data, status, headers, config) {
			console.log("Save returned: " + status);
			console.log(data);
		});
	};

	var createObject = function(url, data){
		$http.post(url, data).success(function(data, status, headers, config) {
			console.log("Created!");
		}).error(function(data, status, headers, config) {
			console.log("Create returned: " + status);
			console.log(data);
		});
	};

	this.save = function(){
		//Make json object for save

		var make_comma_string = function(strings){
			return strings.join(',');
		};

		var obj = {
		    "name": c.name, 
		    "alignment": c.alignment, 
		    "char_class": c.char_class,
		    "level": c.level, 
		    "deity": c.deity, 
		    "homeland": c.homeland, 
		    "race": c.race, 
		    "gender": c.gender.charAt(0), 
		    "size": String(c.size_mod), 
		    "age": c.age, 
		    "height": c.height, 
		    "weight": c.weight, 
		    "hair": c.hair, 
		    "eyes": c.eyes, 
		    "hp_total": c.hp, 
		    "current_hp": c.current_hp,    
		    "xp": c.xp + "," + c.next_level,    
		    "base_attack": c.base_attack, 
		    "init_mod": c.init_mod, 
		    "damage_reduction": c.dr, 
		    "spell_resist": c.spell_resist,
		    "languages": c.languages 
		};

		//Join scores 
		for (var i in abilities_order){
			var abil = abilities_order[i];
			var new_str = c[abil].score + "," + c[abil].temp;
			obj[abil + "_score"] = new_str;
		}

		//Join AC
		obj.ac_mods = make_comma_string([c.ac.armor, c.ac.shield, c.ac.nat, c.ac.deflect, c.ac.misc]);

		//Join Saves
		obj.fort_save = make_comma_string([c.fort.base, c.fort.magic, c.fort.misc, c.fort.temp]);
		obj.reflex_save = make_comma_string([c.reflex.base, c.reflex.magic, c.reflex.misc, c.reflex.temp]);
		obj.will_save = make_comma_string([c.will.base, c.will.magic, c.will.misc, c.will.temp]);

		//Join Skills
		for (var j in skills_order){
			var skill = skills_order[j];
			var skill_name = skill[0];
			var skill_abil = skill[1];
			var skill_model = skill[2];
			var skill_extra = skill[3];

			for (var k in c.skills){
				var skill_obj = c.skills[k];
				if (skill_obj.name === skill_name){
					var class_skill = 0;
					if (skill_obj.c_skill){
						class_skill = 1;
					}
					var skill_data = [class_skill, skill_obj.ranks, skill_obj.misc];
					obj[skill_model] = make_comma_string(skill_data);

					if(skill_extra !== undefined){
						obj[skill_extra] = skill_obj.extra;
					}
					break;
				}
			}
		}

		//Join speeds
		var speed_data = [c.speeds.base, c.speeds.armor, c.speeds.fly, c.speeds.swim, c.speeds.climb, c.speeds.burrow];
		obj.speed = make_comma_string(speed_data);

		//Feats
		obj.feats = c.feats;
		obj.custom_feats = make_comma_string(c.custom_feats);

		//Weapons
		
		for(var l in c.weapons){
			var weapon_data = c.weapons[l];
			if(weapon_data.slug !== undefined){
				//update the weapon
				var url = weapon_api_url + weapon_data.slug;
				updateObject(url, weapon_data);
			}
		}

		//Spell Schools
		for(var m in c.spell_schools){
			var school_data = c.spell_schools[m];
			if(school_data.slug !== undefined){
				//update the school
				var school_url = spell_school_api_url + school_data.slug;
				var update_obj = {
					name: school_data.name,
					spell_mod: school_data.spell_mod,
					known_spells: make_comma_string(school_data.known_spells),
					spells_per_day: make_comma_string(school_data.spells_per_day),
					bonus_spells: make_comma_string(school_data.bonus_spells)
				};
				updateObject(school_url, update_obj);
			}
		}

		//money and loot
		obj.money = make_comma_string([c.money.platinum, c.money.gold, c.money.silver, c.money.copper]);
		obj.loot = c.loot;

		obj.description = c.desc;
		obj.notes = c.notes;

		console.log(obj);

		//actually save the object to the db
		$http.patch(api_url, obj).success(function(data, status, headers, config) {
			console.log("Saved!");
			$("#save-button").text("Saved!");
			setTimeout(function() {
			     // Do something after 3 seconds
			     $("#save-button").text("Save Character");
			}, 2000);
		}).error(function(data, status, headers, config) {
			console.log("Save returned: " + status);
			console.log(data);
		});
    
		/*
		    "items": [], 
		    "special_abilities": [], 
		    "custom_special": ""
		*/

	};
});


app.controller('CharacterController', function($scope, $location, characterService){
	var api_url = "/api/";

	var path = $location.path();
	var slug = path.split("/")[1];
	var character_url = api_url + "characters/" + slug;

	var size_mods = {
        'Colossal': -8,
        'Gargantuan': -4,
        'Huge': -2,
        'Large': -1,
        'Medium': 0,
        'Small': 1,
        'Tiny': 2,
        'Diminutive': 4,
        'Fine': 8
    };

	var isInt = function(x){
		return (typeof x === 'number') && (x % 1 === 0);
	};

	var feats = new Bloodhound({
	  datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
	  queryTokenizer: Bloodhound.tokenizers.whitespace,
	  limit: 10,
	  prefetch: {
	    url: '/api/resources/feats',
	    filter: function(data) {
	      return data.results;
	    }
	  }
	});

	// kicks off the loading/processing of `local` and `prefetch`
	feats.initialize();
	 
	// passing in `null` for the `options` arguments will result in the default
	// options being used
	$('#featprefetch .typeahead').typeahead(null, {
	  name: 'feats',
	  displayKey: 'name',
	  // `ttAdapter` wraps the suggestion engine in an adapter that
	  // is compatible with the typeahead jQuery plugin
	  source: feats.ttAdapter()
	});

	var spells = new Bloodhound({
	  datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
	  queryTokenizer: Bloodhound.tokenizers.whitespace,
	  limit: 10,
	  prefetch: {
	    url: '/api/resources/spells',
	    filter: function(data) {
	      return data.results;
	    }
	  }
	});

	spells.initialize();

	$scope.spellOptions = {
		highlight: true
	};

	$scope.spellData = {
	    displayKey: 'name',
	    source: spells.ttAdapter()
	};

	$scope.c = characterService.getCharacter(character_url);
	$scope.abils = characterService.get_abil_order();
	$scope.size_options = Object.keys(size_mods);
	$scope.genders = ["Male", "Female", "Other"];
	$scope.alignments = ["LG", "NG", "CG", "LN", "N", "CN", "LE", "NE", "CE"];
	$scope.spell_mods = ["Intelligence", "Wisdom", "Charisma"];

	$scope.updateAbil = function(abil, new_values){
		if(isInt(new_values.score) && isInt(new_values.temp)){
			characterService.updateAbil(abil, new_values);
		}
	};

	$scope.updateSkills = function(){
		characterService.updateSkills();
	};

	$scope.updateSaves = function(){
		characterService.updateSaves();
	};

	$scope.updateAC = function(){
		characterService.updateAC();
	};

	$scope.updateSize = function(new_size){
		var new_mod = size_mods[new_size];
		characterService.updateSizeMod(new_mod);
	};

	$scope.updateBAB = function(){
		characterService.updateBAB();
	};

	$scope.saveChar = function(){
		characterService.save();
	};

	$scope.updateHP = function(){
		characterService.calculate_hp_percent();
	};

	$scope.addFeat = function(){
		var new_feat = $('#featfield').val();
		// Check if feat is in list
	    var match = false;
	    for (var i = feats.index.datums.length - 1; i >= 0; i--) {
	        if (new_feat == feats.index.datums[i].name) {
	            match = true;
	        }
	    }
	    if (!match) {
	    	//Add as a custom feat
	    	characterService.addCustomFeat(new_feat);
	    } else {	
			characterService.addFeat(new_feat);
		}
		$('#featfield').val("");
	};

	$scope.deleteFeat = function(feat){
		characterService.deleteFeat(feat);
	};

	$scope.deleteCustomFeat = function(feat){
		characterService.deleteCustomFeat(feat);
	};

	$scope.addWeapon = function(){
		characterService.addWeapon();
	};

	$scope.deleteWeapon = function(weapon){
		characterService.deleteWeapon(weapon);
	};

	$scope.updateSpellMod = function(school){
		characterService.updateSpellMod(school);
	};

	$scope.addSchool = function(school_name){
		characterService.addSchool(school_name);
	};

	$scope.deleteSchool = function(school){
		characterService.deleteSchool(school);
	};

	$scope.addSpell = function(school){
		var new_spell = school.new_spell_name;
		var new_spell_level = parseInt(school.new_spell_level);
		console.log(new_spell);
		console.log(new_spell_level);
		var spell_obj;

		if(typeof new_spell === "string" || new_spell instanceof String){
			//Add as a custom spell
	    	spell_obj = {
	    		school: school.id,
	    		custom_spell: new_spell,
	    		spell_level: new_spell_level
	    	};
	    	characterService.addSpell(spell_obj, school);
		} else {
			spell_obj = {
	    		school: school.id,
	    		spell: new_spell.name,
	    		spell_level: new_spell_level
	    	};
			characterService.addSpell(spell_obj, school);
		}
		school.new_spell_name = "";
		school.new_spell_level = "";
	};

	$('.weapon-details').sortable({
		items: "li:not(.add-area)",
		placeholder: "ui-sortable-placeholder"
	});

	$('.text-area').autosize();
});


app.factory("flash", function(){
	var currentMessage = "";

	return {
		setMessage: function(message) {
			currentMessage = message;
		},
		getMessage: function(){
			return currentMessage;
		}
	};
});

app.controller('CharactersController', function($scope, $http, flash){

	$scope.flash = flash;
	var api_url = "/api/";

	$scope.num_chars = 0;
	$scope.characters = [];
	$scope.user = "";
	$scope.characters_url = "";

	$scope.load_characters = function(){
		$http.get($scope.characters_url).success(function(data){
			$scope.num_chars = data.count;
			$scope.characters = data.results;
		}).error(function(data){
			console.log("Error: " + data);
		});
	};

	$http.get(api_url + "current").success(function(data){
		$scope.user = data.username;
		$scope.characters_url = api_url + "users/" + $scope.user + "/charactersheets";
		$scope.load_characters();
	}).error(function(data){
		console.log("Error: " + data);
	});


	$scope.deleteChar = function(c){
		if (confirm('Are you sure you want to delete this characer: ' + c.name + '?')) {
    		// Delete it!
    		var url = api_url + "characters/" + c.slug;
    		$http.delete(url).success(function(data, status, headers, config) {
				flash.setMessage("Successfully deleted character " + c.name);	
				$scope.load_characters();
			}).error(function(data, status, headers, config) {
				alert("Create returned: " + status);
				console.log(data);
			});
		} 
	};

	var create_api_url = "/api/characters/create";
	$scope.char = {};
	$scope.createChar = function(){

		$http.post(create_api_url, $scope.char).success(function(data, status, headers, config) {
			flash.setMessage("Successfully created character " + $scope.char.name);
			var character_slug = data.slug;
			$scope.char = {};
			$scope.load_characters();
		}).error(function(data, status, headers, config) {
			alert("Create returned: " + status);
			console.log(data);
		});
	};
	
});
