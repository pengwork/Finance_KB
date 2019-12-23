# 测试neo4j的连通性，链接neo4j

from py2neo import Graph,Node,Relationship,NodeMatcher

class Query():
    def __init__(self):
        self.graph=Graph("http://localhost:7474", username="neo4j",password="123")

    # 问题类型0，查询王斌的公司
    def run(self,cql):
        # find_rela  = test_graph.run("match(n:Person)-[:employ_of]->(c:Company) where n.name='王斌' return c.name")
        result=[]
        find_rela = self.graph.run(cql)
        for i in find_rela:
            result.append(i.items()[0][1])
        return result




# if __name__ == '__main__':
#     SQL=Query()
#     result=SQL.run("match(n:Person)-[:employ_of]->(c:Company) where n.name='王斌' return c.name")
#     print(result)
