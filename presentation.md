Consulta com debug.
```
{
  allThemes {
    edges {
      node {
        id
        name
      }
    }
  }

  __debug {
    sql {
      rawSql
    }
  }
}
```

Paginação
```
{
  allThemes(first: 2) {
    edges {
      node {
        id
        name
      }
    }
    pageInfo {
      hasNextPage
      hasPreviousPage
      startCursor
      endCursor
    }
  }
  __debug {
    sql {
      rawSql
    }
  }
}
```

Mutation com erro
```
mutation teste {
  project(input: {name: "Project X", description: "description teste", bounds: "Point", thumbnail: ""}) {
    id
    name
    errors {
      field
      messages
    }
  }
}
```