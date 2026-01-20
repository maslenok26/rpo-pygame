from . import types

# ПАРАМЕТРЫ РАЗРЕШЕНИЯ
GAME_WIDTH = 320
GAME_HEIGHT = 240
HEIGHTS = {'HD': 720, 'FHD': 1080, 'QHD': 1440, 'UHD': 2160}
RESOLUTION = 'HD'
START_SCREEN_SIZE = (HEIGHTS[RESOLUTION] * (16 / 9), HEIGHTS[RESOLUTION])
LETTERBOXING = True

# ПАРАМЕТРЫ ФИЗИКИ
SUB_STEP_LIMIT = 10
EPSILON = 1e-3

# ПАРАМЕТРЫ СМЕНЫ КАДРОВ
FPS_LOCK = True
FPS = 60

# ПАРАМЕТРЫ СПРАЙТОВ
TILE_SIZE = 16
LAYERS: types.Layers = {
    'WALL_FACE': 0,
    'ENEMY': 2,
    'PLAYER': 6,
    'PROJECTILE': 8,
    'WALL_TOP': 9
}


# ПАРАМЕТРЫ ВЗАИМОДЕЙСТВИЯ
COMBAT_RULES: types.CombatRules = {
    'player': {
        'proj_self_group_key': 'player_projectiles',
        'proj_target_group_keys': ('enemies', 'player')
    },
    'enemy': {
        'proj_self_group_key': 'enemy_projectiles',
        'proj_target_group_keys': ('player',)
    }
}

# ХАРАКТЕРИСТИКИ ОБЪЕКТОВ
WEAPON_STATS: types.WeaponStats = {
    'pistol': {
        'cooldown': 150,
        'orbit_offset': (8, 3),
        'muzzle_offset': (9, -2),
        'holstered_offset': (-2, -8),
        'proj_type_key': 'projectile',
        'proj_stats': {
            'speed': 150,
            'damage': 10,
            'lifetime': 3000
        }
    },
    'shotgun': {
        'cooldown': 300,
        'orbit_offset': (3, 4),
        'muzzle_offset': (19, -2),
        'holstered_offset': (0, -4),
        'proj_type_key': 'projectile',
        'proj_stats': {
            'speed': 150,
            'damage': 40,
            'lifetime': 1800
        }
    }
}

PROJECTILE_STATS: types.ProjectileStats = {
    'projectile': {
        'hitbox_size': (4, 4)
    }
}