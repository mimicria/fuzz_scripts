import dnf
import graphviz

def quote_dep(dep):
    without_quotes = dep.name.replace(':', '-')
    return(without_quotes)


base = dnf.Base()
base.read_all_repos()
base.fill_sack(load_system_repo=True, load_available_repos=True)
installed = base.sack.query().installed()

# Создаем граф
graph = graphviz.Digraph(comment='Dependences')

for package in installed:
    # Добавляем узел
    graph.node(package.name)
    # Добавляем зависимости
    for dep in package.requires:
        dep_name = quote_dep(dep)
        graph.edge(package.name, dep_name)

graph.format = 'pdf'
graph.render('dependencies', view=False)