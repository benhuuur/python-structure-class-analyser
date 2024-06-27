Try to get class diagram and flow diagram from directory

- Try to get type from varible assignment (check)
- Try make keys from json be a name of the class
- Make finder inside a directory
- Verify when has list in attributes, generate a erro. (bases topic) 


O código fornecido já está bem estruturado e segue boas práticas em muitos aspectos. No entanto, aqui estão algumas sugestões para melhorar ainda mais a clareza e a manutenção do código:

Padrão de Nomenclatura:

As variáveis e métodos seguem um padrão claro de nomenclatura, o que é bom. No entanto, é sempre útil revisar e garantir consistência:
Nome de variáveis como statement, node, elt, target, file_path, AST_tree são descritivos e claros.
Evitar abreviações excessivas ou nomes muito genéricos é importante para facilitar a leitura e a manutenção do código.
Comentários:

Embora o código seja bastante claro, adicionar comentários breves em trechos mais complexos pode ajudar na compreensão, especialmente em métodos privados como _get_assignment_names, _get_assignment_encapsulation, _get_assignment_data_type, onde a lógica pode não ser imediatamente óbvia para quem está lendo.

Organização e Estrutura:
A estrutura de classes e funções está bem organizada. Certifique-se de que as responsabilidades estão claramente divididas entre os métodos estáticos da classe AST_handler.
Pode ser útil agrupar métodos relacionados mais próximos uns dos outros para facilitar a referência cruzada e a manutenção.

Documentação:
As docstrings estão presentes e descrevem adequadamente a funcionalidade de cada método. Verifique se elas cobrem todas as informações necessárias para entender como usar cada método.

Melhorias Potenciais:
- Considerar a adição de tratamento para casos mais complexos de AST, como expressões lambda ou compreensões de lista, dependendo dos requisitos específicos do projeto.
- Adicionar comentários onde a lógica não é trivial, por exemplo, explicando a lógica por trás da determinação do tipo de dado em _get_assignment_data_type().