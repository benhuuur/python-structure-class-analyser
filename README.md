Try to get class diagram and flow diagram from directory

- Try to get type from varible assignment (check)
- Try make keys from json be a name of the class
- Make finder inside a directory
- Verify when has list in attributes, generate a erro. (bases topic) 

Organização e Estrutura:
-A estrutura de classes e funções está bem organizada. Certifique-se de que as responsabilidades estão claramente divididas entre os métodos estáticos da classe AST_handler.
-Pode ser útil agrupar métodos relacionados mais próximos uns dos outros para facilitar a referência cruzada e a manutenção.

Documentação:
-As docstrings estão presentes e descrevem adequadamente a funcionalidade de cada método. Verifique se elas cobrem todas as informações necessárias para entender como usar cada método.

Melhorias Potenciais:
- Considerar a adição de tratamento para casos mais complexos de AST, como expressões lambda ou compreensões de lista, dependendo dos requisitos específicos do projeto.
- Adicionar comentários onde a lógica não é trivial, por exemplo, explicando a lógica por trás da determinação do tipo de dado em _get_assignment_data_type().