from evaluation.evaluate import build_engine
def test_budget_ram_stock():
    b=build_engine().answer("Suggest an in-stock laptop under INR 70000 with at least 16GB RAM")
    assert "L102" in b["answer"]
    assert "₹68,000" in b["answer"]
def test_monitor_filter():
    b=build_engine().answer("Show a 27-inch monitor below INR 15000")
    assert "M204" in b["answer"]
def test_policy():
    b=build_engine().answer("Can I return an opened headset?")
    assert "unless they are defective" in b["answer"]
    assert "page" in b["sources"][0]
def test_abstain():
    b=build_engine().answer("Recommend a mechanical keyboard below INR 3000")
    assert "No matching product" in b["answer"]
