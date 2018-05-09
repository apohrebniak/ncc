import sys

import ncc.common as cmn

"""deprecated"""
class Action:
    def __init__(self, aState=None, label=None, bState=None, toStack=None,
        eq=None, neq=None):
        self.aState = aState
        self.label = label
        self.bState = bState
        self.toStack = toStack
        self.eq = eq
        self.neq = neq


"""Parser finite-state machine"""


class ParserAuto:
    def __init__(self, tokens, idsTable, constTable):
        self.tokens = tokens
        self.ids = idsTable
        self.consts = constTable
        self.symbols = {v: k for k, v in cmn.SYMBOLS.items()}
        self.words = {v: k for k, v in cmn.WORDS.items()}
        self.stack = list()
        self.actionError = "ERROR"
        self.actionExit = "EXIT"
        self.stateActions = {
            1: [Action(aState=1, label=cmn.SYMBOLS["{"], bState=2, toStack=None,
                       neq=self.actionError)],
            2: [Action(aState=2, label=cmn.SYMBOLS["}"], bState=None,
                       toStack=None, eq=self.actionExit,
                       neq=Action(bState=201, toStack=3))],
            3: [Action(aState=3, label=cmn.SYMBOLS["\n"], bState=201,
                       toStack=3),
                Action(aState=3, label=cmn.SYMBOLS["}"], neq=self.actionError,
                       eq=self.actionExit)],
            201: [Action(aState=201, label=cmn.WORDS["if"], bState=401,
                         toStack=203),
                  Action(aState=201, label=cmn.WORDS["while"], bState=401,
                         toStack=208),
                  Action(aState=201, label=cmn.WORDS["int"], bState=210),
                  Action(aState=201, label=cmn.WORDS["float"], bState=210),
                  Action(aState=201, label=cmn.ID, bState=213),
                  Action(aState=201, label=cmn.WORDS["in"], bState=215),
                  Action(aState=201, label=cmn.WORDS["out"], bState=215),
                  Action(aState=201, label=cmn.SYMBOLS["{"], bState=2,
                         toStack=None, neq=self.actionError)],
            203: [Action(aState=203, label=cmn.SYMBOLS["?"], bState=1,
                         toStack=205, neq=self.actionError)],
            205: [Action(aState=205, label=cmn.SYMBOLS[":"], bState=1,
                         toStack=206, neq=self.actionError)],
            206: [Action(aState=206, label=None, bState=None, toStack=None,
                         eq=self.actionExit)],
            208: [
                Action(aState=208, label=cmn.WORDS["do"], bState=1, toStack=209,
                       neq=self.actionError)],
            209: [Action(aState=209, label=None, bState=None, toStack=None,
                         eq=self.actionExit)],
            210: [Action(aState=210, label=cmn.ID, bState=211, toStack=None,
                         neq=self.actionError)],
            211: [Action(aState=211, label=cmn.SYMBOLS["="], bState=301,
                         toStack=212, neq=self.actionExit)],
            212: [Action(aState=212, label=None, bState=301, toStack=None,
                         eq=self.actionExit)],
            213: [Action(aState=213, label=cmn.SYMBOLS["="], bState=301,
                         toStack=214, neq=self.actionError)],
            214: [Action(aState=214, label=None, bState=None, toStack=None,
                         eq=self.actionExit)],
            215: [Action(aState=215, label=cmn.SYMBOLS["("], bState=501,
                         toStack=217, neq=self.actionError)],
            217: [Action(aState=217, label=cmn.SYMBOLS[")"], bState=None,
                         toStack=None, neq=self.actionError,
                         eq=self.actionExit)],
            301: [Action(aState=301, label=cmn.ID, bState=302),
                  Action(aState=301, label=cmn.CONST, bState=302),
                  Action(aState=301, label=cmn.SYMBOLS["-"], bState=303),
                  Action(aState=301, label=cmn.SYMBOLS["("], bState=301,
                         toStack=304, neq=self.actionError)],
            302: [Action(aState=302, label=cmn.SYMBOLS["+"], bState=301),
                  Action(aState=302, label=cmn.SYMBOLS["-"], bState=301),
                  Action(aState=302, label=cmn.SYMBOLS["/"], bState=301),
                  Action(aState=301, label=cmn.SYMBOLS["*"], bState=301,
                         neq=self.actionExit)],
            303: [Action(aState=303, label=cmn.ID, bState=302),
                  Action(aState=303, label=cmn.CONST, bState=302),
                  Action(aState=303, label=cmn.SYMBOLS["("], bState=301,
                         toStack=304, neq=self.actionError)],
            304: [Action(aState=304, label=cmn.SYMBOLS[")"], bState=302,
                         neq=self.actionError)],
            401: [Action(aState=401, label=cmn.WORDS["not"], bState=401),
                  Action(aState=401, label=cmn.SYMBOLS["["], bState=401,
                         toStack=404,
                         neq=Action(bState=301, toStack=402))],
            402: [Action(aState=402, label=cmn.SYMBOLS["<"], bState=301,
                         toStack=403),
                  Action(aState=402, label=cmn.SYMBOLS["<="], bState=301,
                         toStack=403),
                  Action(aState=402, label=cmn.SYMBOLS[">"], bState=301,
                         toStack=403),
                  Action(aState=402, label=cmn.SYMBOLS[">="], bState=301,
                         toStack=403),
                  Action(aState=402, label=cmn.SYMBOLS["=="], bState=301,
                         toStack=403),
                  Action(aState=402, label=cmn.SYMBOLS["!="], bState=301,
                         toStack=403, neq=self.actionError)],
            403: [Action(aState=403, label=cmn.WORDS["and"], bState=401),
                  Action(aState=403, label=cmn.WORDS["or"], bState=401,
                         neq=self.actionExit)],
            404: [Action(aState=404, label=cmn.SYMBOLS["]"], bState=403,
                         neq=self.actionError)],
            501: [Action(aState=501, label=cmn.ID, bState=502,
                         neq=self.actionError)],
            502: [Action(aState=502, label=cmn.SYMBOLS[","], bState=501,
                         neq=self.actionExit)]
        }

    def errorAtToken(self, token):
        print("Error at row:", token.row_num)
        sys.exit(1)

    def successExit(self):
        sys.exit(0)

    def parse(self):
        state = 1
        tokenIndex = 0
        isSuccess = False

        while not isSuccess:
            token = self.tokens[tokenIndex]
            actions = self.stateActions[state]

            for action in actions:

                # if label equals
                if action.label == token.tag:
                    # if has next state
                    if action.bState:
                        state = action.bState
                        if action.toStack:
                            self.stack.append(action.toStack)
                        tokenIndex = self.incrementTokenIndex(token, tokenIndex)
                        break
                    # if has no next state
                    elif action.eq:
                        # if action is exit
                        if action.eq == self.actionExit:
                            # if stack is not empty
                            if len(self.stack) != 0:
                                state = self.stack.pop()
                                tokenIndex = self.incrementTokenIndex(token,
                                                                      tokenIndex)
                                break
                            else:
                                self.successExit()
                        # if action is not exit do something
                        else:
                            if action.eq.bState:
                                state = action.eq.bState
                            if action.eq.toStack:
                                self.stack.append(action.eq.toStack)
                            tokenIndex = self.incrementTokenIndex(token,
                                                                  tokenIndex)
                            break


                # if label is equals
                elif not action.label and action.eq:
                    # if action is exit
                    if action.eq == self.actionExit:
                        if len(self.stack) != 0:
                            state = self.stack.pop()
                            break

                # if label is not equals
                elif action.neq:
                    # if action is err
                    if action.neq == self.actionError:
                        self.errorAtToken(token)
                    elif action.neq == self.actionExit:
                        if len(self.stack) != 0:
                            state = self.stack.pop()
                            break
                    # if action is not err do something
                    else:
                        if action.neq.bState:
                            state = action.neq.bState
                        if action.neq.toStack:
                            self.stack.append(action.neq.toStack)
                        break
                        # TODO: if not equals

    def incrementTokenIndex(self, token, tokenIndex):
        if tokenIndex + 1 >= len(self.tokens):
            self.errorAtToken(token)
        else:
            return tokenIndex + 1
