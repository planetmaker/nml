from nml import expression, generic
from nml.actions import actionA, action5


class ReplaceSprite(object):
    """
    AST node for a 'replace' block.
    NML syntax: replace(start_id[, default_file]) { ..real sprites.. }

    @ivar param_list: List of parameters passed to the replace-block
    @type param_list: C{list} of L{Expression}

    @ivar sprite_list: List of real sprites to use
    @type sprite_list: Heterogeneous C{list} of L{RealSprite}, L{TemplateUsage}

    @ivar pos: Position information of the 'replace' block.
    @type pos: L{Position}

    @ivar start_id: First sprite to replace. Extracted from C{param_list} during pre-processing.
    @type start_id: C{int}

    @ivar pcx: Default image file to use for sprites. Extracted from C{param_list} during pre-processing.
    @type pcx: C{None} if not specified, else L{StringLiteral}
    """
    def __init__(self, param_list, sprite_list, pos):
        self.param_list = param_list
        self.sprite_list = sprite_list
        self.pos = pos

    def pre_process(self):
        num_params = len(self.param_list)
        if not (1 <= num_params <= 2):
            raise generic.ScriptError("replace-block requires 1 or 2 parameters, encountered " + str(num_params), self.pos)
        self.start_id = self.param_list[0].reduce_constant().value
        if num_params >= 2:
            self.pcx = self.param_list[1].reduce()
            if not isinstance(self.pcx, expression.StringLiteral):
                raise generic.ScriptError("replace-block parameter 2 'file' must be a string literal", self.pcx.pos)
        else:
            self.pcx = None

    def debug_print(self, indentation):
        print indentation*' ' + 'Replace sprites starting at', self.start_id
        print (indentation+2)*' ' + 'Source:', self.pcx.value if self.pcx is not None else 'None'
        print (indentation+2)*' ' + 'Sprites:'
        for sprite in self.sprite_list:
            sprite.debug_print(indentation + 4)

    def get_action_list(self):
        return actionA.parse_actionA(self)

class ReplaceNewSprite(object):
    """
    AST node for a 'replacenew' block.
    NML syntax: replacenew(type[, default_file[, offset]]) { ..real sprites.. }

    @ivar param_list: List of parameters passed to the replacenew-block
    @type param_list: C{list} of L{Expression}

    @ivar sprite_list: List of real sprites to use
    @type sprite_list: Heterogeneous C{list} of L{RealSprite}, L{TemplateUsage}

    @ivar pos: Position information of the 'replacenew' block.
    @type pos: L{Position}

    @ivar type: Type of sprites to replace. Extracted from C{param_list} during pre-processing.
    @type type: L{Identifier}

    @ivar pcx: Default image file to use for sprites. Extracted from C{param_list} during pre-processing.
    @type pcx: C{None} if not specified, else L{StringLiteral}

    @ivar offset: Offset into the block of sprites. Extracted from C{param_list} during pre-processing.
    @type offset: C{int}
    """
    def __init__(self, param_list, sprite_list, pos):
        self.param_list = param_list
        self.sprite_list = sprite_list
        self.pos = pos

    def pre_process(self):
        num_params = len(self.param_list)
        if not (1 <= num_params <= 3):
            raise generic.ScriptError("replacenew-block requires 1 to 3 parameters, encountered " + str(num_params), self.pos)

        self.type = self.param_list[0]
        if not isinstance(self.type, expression.Identifier):
            raise generic.ScriptError("replacenew parameter 'type' must be an identifier of a sprite replacement type", self.type.pos)
            

        if num_params >= 2:
            self.pcx = self.param_list[1].reduce()
            if not isinstance(self.pcx, expression.StringLiteral):
                raise generic.ScriptError("replacenew-block parameter 2 'file' must be a string literal", self.pcx.pos)
        else:
            self.pcx = None

        if num_params >= 3:
            self.offset = self.param_list[2].reduce_constant().value
            generic.check_range(self.offset, 0, 0xFFFF, "replacenew-block parameter 3 'offset'", self.param_list[2].pos)
        else:
            self.offset = 0

    def debug_print(self, indentation):
        print indentation*' ' + 'Replace sprites for new features of type', self.type
        print (indentation+2)*' ' + 'Offset:  ', self.offset
        print (indentation+2)*' ' + 'Source:  ', self.pcx.value if self.pcx is not None else 'None'
        print (indentation+2)*' ' + 'Sprites:'
        for sprite in self.sprite_list:
            sprite.debug_print(indentation + 4)

    def get_action_list(self):
        return action5.parse_action5(self)
