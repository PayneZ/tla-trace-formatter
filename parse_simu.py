from lark import Lark, Transformer, v_args
import html

LINE_SEP = "<br />"

class State:
    def __init__(self, name, variables):
        self.name = name
        self.variables = variables

    def __str__(self):
        return "{0}\n{1}".format(
            self.name,
            " ".join("{0} = {1}".format(k, v) for k, v in self.variables.items()))

    def __repr__(self):
        return self.__str__()

class TreeToStates(Transformer):
    def __init__(self, text):
        self.text = text

    @v_args(meta=True)
    def show_text(self, children, meta):
        text = self.text[children.start_pos:children.end_pos] if not children.empty else ""
        print(text)
        return html.escape(text).replace("\n", LINE_SEP)

    def value(self, children):
        return children[0]

    function_kv_print = show_text
    function = show_text
    word = show_text
    sequence = show_text
    state_name = show_text
    set = show_text
    # behavior is a list of states.
    behavior = list

    def function_print(self, children):
        return LINE_SEP.join(children)

    def state(self, children):
        name = children[0]
        variables = {v.children[0]: v.children[1] for v in children[1:]}
        return State(name, variables)

if __name__ == "__main__":
    with open("tla-simluate-grammar.lark", "r") as grammar:
        parser = Lark(grammar, start='behavior', propagate_positions=True)
        with open("simu_0_0", "r") as f:
            text = f.read()
            tree = parser.parse(text)
            result = TreeToStates(text).transform(tree)
            #print(result)
