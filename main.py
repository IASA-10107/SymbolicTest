from symbolic_base import *
from typing import Any
import streamlit as st

st.title("미분기? v0.1.0")

project_path = "\\"

doc = st.sidebar
chat, code, changelog = st.tabs(["미분기", "CODE", "CHANGELOG"])

with doc:
    doc_path = "doc.md"
    __doc: str
    with open(project_path+doc_path, mode="r", encoding="utf-8") as file:
        __doc = file.read()
    st.write(__doc)

with chat:

    reload = st.button("Reload")

    symbol_tab = st.expander(f"**Add Symbols**")
    with symbol_tab:
        symbol_input = st.text_input("Symbol")
        symbol_add = st.button("Register")
        if symbol_add:
            if not symbol_input.isidentifier():
                raise NameError("Invaid name for Symbol (Try name able to be used in identifier)")
            else:
                Symbol(symbol_input)
        
        __symbol_content = ", ".join(Symbol.symbols)
        st.write(f"**Current Symbols: [{__symbol_content}]**")

    term_input = st.text_input("Term to Differentiate")
    term_base = st.selectbox("Differential Base", Symbol.symbols.keys())
    term_add = st.button("Do!")
    if term_add:
        term: Term = eval(term_input, None, Symbol.symbols)
        if not isinstance(term, Term): raise SyntaxError("invalid syntax")
        else:
            st.write(term)
            st.write(compress(term.diff(Symbol.symbols[term_base])))

with code:
    st.header("코드")
    code_paths = ["symbolic_base.py", "main.py"]
    for path in code_paths:
        __tab = st.expander(f"**{path}**")
        __code: str
        with open(project_path+path, mode="r", encoding="utf-8") as file:
            __code = file.read()
        __tab.code(__code)
    
    doc_paths = ["idea.md"]
    for path in doc_paths:
        __tab = st.expander(f"**{path}**")
        __doc: str
        with open(project_path+path, mode="r", encoding="utf-8") as file:
            __doc = file.read()
        __tab.write(__doc)

with changelog:
    changelog_path = "version.md"
    __version: str
    with open(project_path+changelog_path, mode="r", encoding="utf-8") as file:
        __version = file.read()
    st.write(__version)

console = st.chat_input("**DO NOT USE** (RAW CONSOLE ONLY FOR DEBUG)")
exec(f"{console}")
