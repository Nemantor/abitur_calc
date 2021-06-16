var input_lis = document.getElementsByTagName("input");

for (var i = 0; i < input_lis.length; i++) {
  input_lis[i].setAttribute("inputmode", "decimal");
}

function validate() {
  if (document.getElementById("mun2_abi").value != "non") {
    if (document.getElementById("mundlich_2").value == 0) {
      alert("input 2.mündliche");
      document.getElementById("mundlich_2").required = true;
      return false;
    }
  } else {
    document.getElementById("mundlich_2").required = false;
  }

  if (
    document.getElementById("sch_abi").value == "Phy" &&
    document.getElementById("phy_ab").value == 0
  ) {
    alert("Enter Physik Abitur Note");
    document.getElementById("phy_ab").required = true;
    return false;
  }
  if (
    document.getElementById("sch_abi").value == "Bio" &&
    document.getElementById("bio_ab").value == 0
  ) {
    alert("Enter Biologie Abitur Note");
    document.getElementById("bio_ab").required = true;
    return false;
  }
  if (
    document.getElementById("sch_abi").value == "Chemie" &&
    document.getElementById("che_ab").value == 0
  ) {
    alert("Enter Chemie Abitur Note");
    document.getElementById("che_ab").required = true;
    return false;
  }

  if (
    document.getElementById("mun2_abi").value ==
    document.getElementById("mun_abi").value
  ) {
    alert("You can't select two mündliche from the same unterricht");
    return false;
  }
  var input_list = document.getElementsByTagName("input");
  for (var i = 0; i < input_list.length; i++) {
    if (input_list[i].value > 15 || input_list[i].value < 0) {
      var etiket = input_list[i].name;
      alert("Enter a valid value:" + etiket);
      return false;
    }
  }

  return true;
}