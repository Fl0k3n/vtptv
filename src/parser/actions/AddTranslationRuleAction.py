from parser.actions.Action import RouterAction

from model.devices.Router import Router
from model.translations.Nat import DNat, OverloadNat, SNat


class AddTranslationRuleAction(RouterAction):
    def __init__(self, rule: OverloadNat | SNat | DNat) -> None:
        super().__init__()
        self.rule = rule

    def apply(self, node: Router) -> None:
        super().apply(node)

        if isinstance(self.rule, SNat):
            node.snat_rules.append(self.rule)
        elif isinstance(self.rule, DNat):
            node.dnat_rules.append(self.rule)
        else:
            node.overload_nat_rules.append(self.rule)

