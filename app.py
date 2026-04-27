import streamlit as st
import io
import sys
import matplotlib.pyplot as plt

import lexer
import parser
import semantic
import codegen
import AstVisual

st.set_page_config(page_title="Pseudocode Compiler", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
}

.stApp {
    background-color: #0d0d0d;
    color: #e8e8e8;
}

h1, h2, h3, h4 {
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 600;
    letter-spacing: -0.5px;
}

.stTextArea textarea {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 14px;
    background-color: #161616;
    color: #e8e8e8;
    border: 1px solid #2e2e2e;
    border-radius: 4px;
}

.stButton > button {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 13px;
    font-weight: 600;
    border-radius: 4px;
    border: none;
    padding: 0.5rem 1.4rem;
    letter-spacing: 0.5px;
}

.stButton > button[kind="primary"] {
    background-color: #c8f250;
    color: #0d0d0d;
}

.stButton > button[kind="primary"]:hover {
    background-color: #d9ff66;
}

.stButton > button[kind="secondary"] {
    background-color: #1e1e1e;
    color: #c8f250;
    border: 1px solid #c8f250;
}

.stTabs [data-baseweb="tab"] {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    color: #888;
    letter-spacing: 0.5px;
}

.stTabs [aria-selected="true"] {
    color: #c8f250;
    border-bottom: 2px solid #c8f250;
}

.stDataFrame {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 13px;
}

.stCode code {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 13px;
    background-color: #161616;
}

.stAlert {
    border-radius: 4px;
}

section[data-testid="stSidebar"] {
    background-color: #111111;
    border-right: 1px solid #1e1e1e;
}

hr {
    border-color: #1e1e1e;
}

.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

st.title("Pseudocode Compiler")
st.caption("Lexical analysis · Syntax parsing · Semantic check · Python generation")

EXAMPLES = {
    "Factorial": """FUNCTION fact(n)
IF n == 0 THEN
RETURN 1
ELSE
RETURN n * fact(n - 1)
END
END

SET result TO fact(5)
PRINT result
""",
    "Fibonacci": """FUNCTION fib(n)
IF n <= 1 THEN
RETURN n
END
RETURN fib(n - 1) + fib(n - 2)
END

PRINT fib(7)
""",
    "Array & For Loop": """ARRAY arr[5]

FOR i FROM 0 TO 4
SET arr[i] TO i * 10
END

FOR j FROM 0 TO 4
PRINT arr[j]
END
""",
    "While Loop & Input": """INPUT x
SET count TO x

WHILE count > 0
PRINT count
SET count TO count - 1
END

PRINT "Done!"
"""
}

with st.sidebar:
    st.markdown("### Examples")
    selected_example = st.selectbox("Choose an example:", list(EXAMPLES.keys()), label_visibility="collapsed")
    if st.button("Load Example", use_container_width=True):
        st.session_state["code_input"] = EXAMPLES[selected_example]


    st.markdown("---")
    st.markdown("### Pipeline")
    st.markdown("""
<small style="color:#888; font-family:'IBM Plex Mono',monospace; line-height:2">
1. Lexer<br>
2. Parser<br>
3. AST Visualization<br>
4. Semantic Analysis<br>
5. Code Generation
</small>
""", unsafe_allow_html=True)

if "code_input" not in st.session_state:
    st.session_state["code_input"] = ""

source_code = st.text_area(
    "Source Input",
    value=st.session_state["code_input"],
    height=280,
    placeholder="Write your pseudocode here...",
)

if st.button("Compile", type="primary"):
    st.session_state["run_compile"] = True

if st.session_state.get("run_compile", False):
    if not source_code.strip():
        st.warning("No input provided.")
        st.session_state["run_compile"] = False
    else:
        tab_lex, tab_parse, tab_ast, tab_sem, tab_gen = st.tabs([
            "Lexer", "Parser", "AST Graph", "Semantic", "Output"
        ])

        has_error = False
        ast = None

        with tab_lex:
            st.subheader("Lexical Analysis")
            lexer.lexer.lineno = 1
            lexer.lexer.errors = 0
            lexer.lexer.errorList = []
            lexer.lexer.input(source_code)

            tokens_data = []
            for token in lexer.lexer:
                val = "newline" if token.value == "\n" else str(token.value)
                tokens_data.append({
                    "Type": token.type,
                    "Value": val,
                    "Line": token.lineno,
                    "Position": token.lexpos
                })

            if lexer.lexer.errors > 0:
                st.error("Lexical errors found.")
                for err in lexer.lexer.errorList:
                    st.write(f"- {err}")
                has_error = True
            else:
                st.success(f"{len(tokens_data)} tokens found.")
                if tokens_data:
                    st.dataframe(tokens_data, use_container_width=True)

            lexer.lexer.lineno = 1
            lexer.lexer.errors = 0
            lexer.lexer.errorList = []
            lexer.lexer.input(source_code)

        if not has_error:
            with tab_parse:
                st.subheader("Syntax Analysis")
                parser.parser.errorList = []

                try:
                    ast = parser.parser.parse(source_code, lexer=lexer.lexer)
                except Exception as e:
                    st.error(f"Parse failed: {e}")
                    has_error = True

                if not has_error:
                    if parser.parser.errorList:
                        st.error("Syntax errors found.")
                        for err in parser.parser.errorList:
                            st.write(f"- {err}")
                        has_error = True
                    elif ast is None:
                        st.error("No AST produced. Check your pseudocode syntax.")
                        has_error = True
                    else:
                        st.success("Parsed successfully.")
                        ast_text = "\n".join(AstVisual.visualizeText(ast))
                        st.code(ast_text, language="text")

        if not has_error and ast is not None:
            with tab_ast:
                st.subheader("AST Graph")
                original_show = plt.show
                plt.show = lambda: None
                try:
                    plt.clf()
                    AstVisual.visualizeGraph(ast)
                    st.pyplot(plt.gcf())
                except Exception as e:
                    st.error(f"Graph generation failed: {e}")
                finally:
                    plt.show = original_show

        if not has_error and ast is not None:
            with tab_sem:
                st.subheader("Semantic Analysis")
                old_stdout = sys.stdout
                sys.stdout = sem_buf = io.StringIO()
                is_valid = semantic.SemanticAnalysis(ast)
                sys.stdout = old_stdout

                if is_valid:
                    st.success("No semantic errors found.")
                else:
                    st.error("Semantic errors detected.")
                    st.code(sem_buf.getvalue(), language="text")
                    has_error = True

        if not has_error and ast is not None:
            with tab_gen:
                st.subheader("Generated Python")
                try:
                    python_code = codegen.CodeGenerator(ast)
                    st.success("Code generated.")
                    st.code(python_code, language="python")

                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            label="Download .py",
                            data=python_code,
                            file_name="output.py",
                            mime="text/x-python",
                            use_container_width=True,
                        )
                    with col2:
                        run_clicked = st.button("Run", type="primary", use_container_width=True)

                    st.divider()
                    st.markdown("#### Terminal")
                    with st.container(border=True):
                        prog_inputs = st.text_area(
                            "STDIN",
                            height=90,
                            placeholder="Program inputs, one per line..."
                        )

                        if run_clicked:
                            input_stream = io.StringIO(prog_inputs)
                            old_stdin = sys.stdin
                            sys.stdin = input_stream

                            output_stream = io.StringIO()
                            old_stdout = sys.stdout
                            sys.stdout = output_stream

                            run_error = None
                            try:
                                exec(python_code, {})
                            except Exception as e:
                                run_error = e
                            finally:
                                sys.stdin = old_stdin
                                sys.stdout = old_stdout

                            st.divider()
                            st.caption("STDOUT")
                            if run_error:
                                st.error(f"Runtime error: {run_error}")
                                st.code(output_stream.getvalue(), language="console")
                            else:
                                out = output_stream.getvalue()
                                st.code(out if out.strip() else "(no output)", language="console")

                except Exception as e:
                    st.error(f"Code generation failed: {e}")