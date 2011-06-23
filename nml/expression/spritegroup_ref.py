from nml import generic
from nml.actions import action2
from .base_expression import Type, Expression

class SpriteGroupRef(Expression):
    """
    Container for a reference to a sprite group / layout

    @ivar name: Name of the referenced item
    @type name: L{Identifier}

    @ivar param_list: List of parameters to be passed
    @type param_list: C{list} of L{Expression}

    @ivar pos: Position of this reference
    @type pos: L{Position}
    """
    def __init__(self, name, param_list, pos):
        self.name = name
        self.param_list = param_list
        self.pos = pos

    def debug_print(self, indentation):
        print indentation*' ' +'Reference to: ' + str(self.name)
        if len(self.param_list) != 0:
            print 'Parameters:'
            for p in self.param_list:
                p.debug_print(indentation + 2)

    def __str__(self):
        if self.param_list:
            return '%s(%s)' % (self.name, ', '.join(str(x) for x in self.param_list))
        return str(self.name)

    def get_action2_id(self):
        """
        Get the action2 set-ID that this reference maps to

        @return: The set ID
        @rtype: C{int}
        """
        if self.name.value == 'CB_FAILED': return 0 # 0 serves as a failed CB result because it is never used
        try:
            spritegroup = action2.resolve_spritegroup(self.name)
        except generic.ScriptError:
            assert False, "Illegal action2 reference '%s' encountered." % self.name.value

        return spritegroup.get_action2().id

    def reduce(self, id_dicts = [], unknown_id_fatal = True):
        return self

    def type(self):
        return Type.SPRITEGROUP_REF