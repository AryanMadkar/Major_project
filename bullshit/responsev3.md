# Model Evaluation Report (All Single-Property Messages)

- Generated: 2026-05-28T16:17:16
- Endpoint: http://127.0.0.1:8000/extract
- Total messages: 16
- Overall supported fields: 91/126
- Overall accuracy: 72.22%

## 1. single_property_Dataset/rent/01.md

- Sample accuracy: 82.35% (14/17)

### Original message

```text
🏢 1BHK FLAT ON RENT 🏢
👉🏻 Available Semi Furnished R Flat 1BHK On Rent at Ganesh Chowk, Charkop, kandivali west,
👉🏻 North Facing, with Gas pipe Line Connection
👉🏻 walking Distance of Kandivali Metro Station
💰 Rent 33000/-   &
Deposit of Rs 1,50,000/-
📞 Please Contact :
BHOOMI ASSOCAITES
9867722289
7977756496
```

### Model response

```json
{
  "amenities": [
    "air conditioning"
  ],
  "attributes": {
    "facing": "north",
    "furnishing": "semi_furnished"
  },
  "extraction_meta": {
    "amenities": {
      "confidence": 75,
      "source": "regex+llm",
      "value": [
        "air conditioning"
      ]
    },
    "attributes.facing": {
      "confidence": 85,
      "source": "keyword",
      "value": "north"
    },
    "attributes.furnishing": {
      "confidence": 80,
      "source": "keyword+scoring",
      "value": "semi_furnished"
    },
    "location.locations": {
      "confidence": 80,
      "source": "dictionary+patterns",
      "value": [
        "charkop",
        "kandivali",
        "kandivali west",
        "metro station"
      ]
    },
    "location.primary_location": {
      "confidence": 80,
      "source": "dictionary+patterns",
      "value": "charkop"
    },
    "location.railway_line": {
      "confidence": 85,
      "source": "dictionary",
      "value": "western"
    },
    "metadata.contact_numbers": {
      "confidence": 95,
      "source": "regex+llm",
      "value": [
        "7977756496",
        "9867722289"
      ]
    },
    "metadata.contact_people": {
      "confidence": 0,
      "source": "llm+cleanup",
      "value": []
    },
    "metadata.message_title": {
      "confidence": 75,
      "source": "llm+rules",
      "value": "Flat"
    },
    "parking.parking_count": {
      "confidence": 0,
      "source": "regex",
      "value": null
    },
    "parking.parking_type": {
      "confidence": 0,
      "source": "keyword",
      "value": null
    },
    "pricing.deposit_price": {
      "confidence": 90,
      "source": "regex+rules",
      "value": 33000
    },
    "pricing.price": {
      "confidence": 85,
      "source": "regex+rules",
      "value": 33000
    },
    "pricing.price_max": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.price_min": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.rent_price": {
      "confidence": 90,
      "source": "regex+rules",
      "value": 1
    },
    "property.all_detected_subtypes": {
      "confidence": 75,
      "source": "keyword+llm",
      "value": [
        "apartment"
      ]
    },
    "property.property_subtype": {
      "confidence": 80,
      "source": "keyword+llm",
      "value": "apartment"
    },
    "summary.bhk": {
      "confidence": 90,
      "source": "regex",
      "value": 1
    },
    "summary.request_type": {
      "confidence": 90,
      "source": "keyword+rules",
      "value": "rent"
    }
  },
  "location": {
    "locations": [
      "charkop",
      "kandivali",
      "kandivali west",
      "metro station"
    ],
    "primary_location": "charkop",
    "railway_line": "western"
  },
  "metadata": {
    "contact_numbers": [
      "7977756496",
      "9867722289"
    ],
    "contact_people": [],
    "message_title": "Flat",
    "metadata_summary": {
      "has_contact": true,
      "total_contacts": 0,
      "total_numbers": 2
    }
  },
  "parking": {
    "parking_count": null,
    "parking_type": null
  },
  "pricing": {
    "deposit_price": 33000,
    "price": 33000,
    "price_max": null,
    "price_min": null,
    "rent_price": 1
  },
  "property": {
    "all_detected_subtypes": [
      "apartment"
    ],
    "property_subtype": "apartment"
  },
  "summary": {
    "bhk": 1,
    "request_type": "rent"
  }
}
```

## 2. single_property_Dataset/rent/02.md

- Sample accuracy: 60.00% (3/5)

### Original message

```text
1 bhk fully furnished in blue empire@36000 negotiable

For more details Contact
Rajan sarawagi
9821452541
```

### Model response

```json
{
  "amenities": [],
  "attributes": {
    "facing": null,
    "furnishing": "fully_furnished"
  },
  "extraction_meta": {
    "amenities": {
      "confidence": 75,
      "source": "regex+llm",
      "value": [
        "air conditioning"
      ]
    },
    "attributes.facing": {
      "confidence": 0,
      "source": "keyword",
      "value": null
    },
    "attributes.furnishing": {
      "confidence": 80,
      "source": "keyword+scoring",
      "value": "fully_furnished"
    },
    "location.locations": {
      "confidence": 0,
      "source": "dictionary+patterns",
      "value": []
    },
    "location.primary_location": {
      "confidence": 0,
      "source": "dictionary+patterns",
      "value": null
    },
    "location.railway_line": {
      "confidence": 0,
      "source": "dictionary",
      "value": null
    },
    "metadata.contact_numbers": {
      "confidence": 95,
      "source": "regex+llm",
      "value": [
        "9821452541"
      ]
    },
    "metadata.contact_people": {
      "confidence": 0,
      "source": "llm+cleanup",
      "value": []
    },
    "metadata.message_title": {
      "confidence": 75,
      "source": "llm+rules",
      "value": "Flat"
    },
    "parking.parking_count": {
      "confidence": 0,
      "source": "regex",
      "value": null
    },
    "parking.parking_type": {
      "confidence": 0,
      "source": "keyword",
      "value": null
    },
    "pricing.deposit_price": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.price": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.price_max": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.price_min": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.rent_price": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "property.all_detected_subtypes": {
      "confidence": 0,
      "source": "keyword+llm",
      "value": []
    },
    "property.property_subtype": {
      "confidence": 80,
      "source": "keyword+llm",
      "value": "apartment"
    },
    "summary.bhk": {
      "confidence": 90,
      "source": "regex",
      "value": 1
    },
    "summary.request_type": {
      "confidence": 90,
      "source": "keyword+rules",
      "value": "unknown"
    }
  },
  "location": {
    "locations": [],
    "primary_location": null,
    "railway_line": null
  },
  "metadata": {
    "contact_numbers": [
      "9821452541"
    ],
    "contact_people": [],
    "message_title": "1 BHK Fully Furnished in Blue Empire",
    "metadata_summary": {
      "has_contact": true,
      "total_contacts": 0,
      "total_numbers": 1
    }
  },
  "parking": {
    "parking_count": null,
    "parking_type": null
  },
  "pricing": {
    "deposit_price": null,
    "price": null,
    "price_max": null,
    "price_min": null,
    "rent_price": null
  },
  "property": {
    "all_detected_subtypes": [],
    "property_subtype": "apartment"
  },
  "summary": {
    "bhk": 1,
    "request_type": "unknown"
  }
}
```

## 3. single_property_Dataset/rent/03.md

- Sample accuracy: 60.00% (3/5)

### Original message

```text
🏠 2 bhk for rent in veena smart homes@49000

Semi furnished flat
Family preferred
```

### Model response

```json
{
  "amenities": [],
  "attributes": {
    "facing": null,
    "furnishing": "fully_furnished"
  },
  "extraction_meta": {
    "amenities": {
      "confidence": 0,
      "source": "regex+llm",
      "value": []
    },
    "attributes.facing": {
      "confidence": 0,
      "source": "keyword",
      "value": null
    },
    "attributes.furnishing": {
      "confidence": 80,
      "source": "keyword+scoring",
      "value": "fully_furnished"
    },
    "location.locations": {
      "confidence": 0,
      "source": "dictionary+patterns",
      "value": []
    },
    "location.primary_location": {
      "confidence": 0,
      "source": "dictionary+patterns",
      "value": null
    },
    "location.railway_line": {
      "confidence": 0,
      "source": "dictionary",
      "value": null
    },
    "metadata.contact_numbers": {
      "confidence": 0,
      "source": "regex+llm",
      "value": []
    },
    "metadata.contact_people": {
      "confidence": 0,
      "source": "llm+cleanup",
      "value": []
    },
    "metadata.message_title": {
      "confidence": 75,
      "source": "llm+rules",
      "value": "Flat"
    },
    "parking.parking_count": {
      "confidence": 0,
      "source": "regex",
      "value": null
    },
    "parking.parking_type": {
      "confidence": 0,
      "source": "keyword",
      "value": null
    },
    "pricing.deposit_price": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.price": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.price_max": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.price_min": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.rent_price": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "property.all_detected_subtypes": {
      "confidence": 75,
      "source": "keyword+llm",
      "value": [
        "apartment"
      ]
    },
    "property.property_subtype": {
      "confidence": 80,
      "source": "keyword+llm",
      "value": "apartment"
    },
    "summary.bhk": {
      "confidence": 90,
      "source": "regex",
      "value": 2
    },
    "summary.request_type": {
      "confidence": 90,
      "source": "keyword+rules",
      "value": "rent"
    }
  },
  "location": {
    "locations": [],
    "primary_location": null,
    "railway_line": null
  },
  "metadata": {
    "contact_numbers": [],
    "contact_people": [],
    "message_title": "Flat",
    "metadata_summary": {
      "has_contact": false,
      "total_contacts": 0,
      "total_numbers": 0
    }
  },
  "parking": {
    "parking_count": null,
    "parking_type": null
  },
  "pricing": {
    "deposit_price": null,
    "price": null,
    "price_max": null,
    "price_min": null,
    "rent_price": null
  },
  "property": {
    "all_detected_subtypes": [
      "apartment"
    ],
    "property_subtype": "apartment"
  },
  "summary": {
    "bhk": 2,
    "request_type": "rent"
  }
}
```

## 4. single_property_Dataset/rent/04.md

- Sample accuracy: 85.71% (6/7)

### Original message

```text
3 bhk on rent in hiranandani heritage, sv road, poisar, @90000

Fully furnished
Higher floor
```

### Model response

```json
{
  "amenities": [],
  "attributes": {
    "facing": null,
    "furnishing": "fully_furnished"
  },
  "extraction_meta": {
    "amenities": {
      "confidence": 0,
      "source": "regex+llm",
      "value": []
    },
    "attributes.facing": {
      "confidence": 0,
      "source": "keyword",
      "value": null
    },
    "attributes.furnishing": {
      "confidence": 80,
      "source": "keyword+scoring",
      "value": "fully_furnished"
    },
    "location.locations": {
      "confidence": 80,
      "source": "dictionary+patterns",
      "value": [
        "sv road",
        "poisar"
      ]
    },
    "location.primary_location": {
      "confidence": 80,
      "source": "dictionary+patterns",
      "value": "sv road"
    },
    "location.railway_line": {
      "confidence": 0,
      "source": "dictionary",
      "value": null
    },
    "metadata.contact_numbers": {
      "confidence": 0,
      "source": "regex+llm",
      "value": []
    },
    "metadata.contact_people": {
      "confidence": 0,
      "source": "llm+cleanup",
      "value": []
    },
    "metadata.message_title": {
      "confidence": 75,
      "source": "llm+rules",
      "value": "Flat"
    },
    "parking.parking_count": {
      "confidence": 0,
      "source": "regex",
      "value": null
    },
    "parking.parking_type": {
      "confidence": 0,
      "source": "keyword",
      "value": null
    },
    "pricing.deposit_price": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.price": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.price_max": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.price_min": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.rent_price": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "property.all_detected_subtypes": {
      "confidence": 0,
      "source": "keyword+llm",
      "value": []
    },
    "property.property_subtype": {
      "confidence": 80,
      "source": "keyword+llm",
      "value": "apartment"
    },
    "summary.bhk": {
      "confidence": 90,
      "source": "regex",
      "value": 3
    },
    "summary.request_type": {
      "confidence": 90,
      "source": "keyword+rules",
      "value": "rent"
    }
  },
  "location": {
    "locations": [
      "sv road",
      "poisar"
    ],
    "primary_location": "sv road",
    "railway_line": null
  },
  "metadata": {
    "contact_numbers": [],
    "contact_people": [],
    "message_title": "Flat",
    "metadata_summary": {
      "has_contact": false,
      "total_contacts": 0,
      "total_numbers": 0
    }
  },
  "parking": {
    "parking_count": null,
    "parking_type": null
  },
  "pricing": {
    "deposit_price": null,
    "price": null,
    "price_max": null,
    "price_min": null,
    "rent_price": null
  },
  "property": {
    "all_detected_subtypes": [],
    "property_subtype": "apartment"
  },
  "summary": {
    "bhk": 3,
    "request_type": "rent"
  }
}
```

## 5. single_property_Dataset/rent/049.md

- Sample accuracy: 55.56% (5/9)

### Original message

```text
2 Bhk Rental Flat In Uk Iridium
Semi Furnished Flat With Modular Kitchen
Rent 45k Deposit 1.25 lakh
```

### Model response

```json
{
  "amenities": [
    "modular kitchen"
  ],
  "attributes": {
    "facing": null,
    "furnishing": "semi_furnished"
  },
  "extraction_meta": {
    "amenities": {
      "confidence": 75,
      "source": "regex+llm",
      "value": [
        "modular kitchen"
      ]
    },
    "attributes.facing": {
      "confidence": 0,
      "source": "keyword",
      "value": null
    },
    "attributes.furnishing": {
      "confidence": 80,
      "source": "keyword+scoring",
      "value": "semi_furnished"
    },
    "location.locations": {
      "confidence": 0,
      "source": "dictionary+patterns",
      "value": []
    },
    "location.primary_location": {
      "confidence": 0,
      "source": "dictionary+patterns",
      "value": null
    },
    "location.railway_line": {
      "confidence": 0,
      "source": "dictionary",
      "value": null
    },
    "metadata.contact_numbers": {
      "confidence": 0,
      "source": "regex+llm",
      "value": []
    },
    "metadata.contact_people": {
      "confidence": 0,
      "source": "llm+cleanup",
      "value": []
    },
    "metadata.message_title": {
      "confidence": 75,
      "source": "llm+rules",
      "value": "Flat"
    },
    "parking.parking_count": {
      "confidence": 0,
      "source": "regex",
      "value": null
    },
    "parking.parking_type": {
      "confidence": 0,
      "source": "keyword",
      "value": null
    },
    "pricing.deposit_price": {
      "confidence": 90,
      "source": "regex+rules",
      "value": 45000
    },
    "pricing.price": {
      "confidence": 85,
      "source": "regex+rules",
      "value": 125000
    },
    "pricing.price_max": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.price_min": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.rent_price": {
      "confidence": 90,
      "source": "regex+rules",
      "value": 125000
    },
    "property.all_detected_subtypes": {
      "confidence": 75,
      "source": "keyword+llm",
      "value": [
        "apartment"
      ]
    },
    "property.property_subtype": {
      "confidence": 80,
      "source": "keyword+llm",
      "value": "apartment"
    },
    "summary.bhk": {
      "confidence": 90,
      "source": "regex",
      "value": 2
    },
    "summary.request_type": {
      "confidence": 90,
      "source": "keyword+rules",
      "value": "rent"
    }
  },
  "location": {
    "locations": [],
    "primary_location": null,
    "railway_line": null
  },
  "metadata": {
    "contact_numbers": [],
    "contact_people": [],
    "message_title": "Flat",
    "metadata_summary": {
      "has_contact": false,
      "total_contacts": 0,
      "total_numbers": 0
    }
  },
  "parking": {
    "parking_count": null,
    "parking_type": null
  },
  "pricing": {
    "deposit_price": 45000,
    "price": 125000,
    "price_max": null,
    "price_min": null,
    "rent_price": 125000
  },
  "property": {
    "all_detected_subtypes": [
      "apartment"
    ],
    "property_subtype": "apartment"
  },
  "summary": {
    "bhk": 2,
    "request_type": "rent"
  }
}
```

## 6. single_property_Dataset/requirements/01.md

- Sample accuracy: 80.00% (8/10)

### Original message

```text
OM SAI RAM
🏠REQUIRED 1 BHK FLAT FOR OUT RATE BUDGET 1 CR TO 1.10 CR
LOCATION ANY CHARKOP SECTOR
KANDIVALI WEST

CALL
9820067788
```

### Model response

```json
{
  "amenities": [],
  "attributes": {
    "facing": null,
    "furnishing": null
  },
  "extraction_meta": {
    "amenities": {
      "confidence": 0,
      "source": "regex+llm",
      "value": []
    },
    "attributes.facing": {
      "confidence": 0,
      "source": "keyword",
      "value": null
    },
    "attributes.furnishing": {
      "confidence": 0,
      "source": "keyword+scoring",
      "value": null
    },
    "location.locations": {
      "confidence": 80,
      "source": "dictionary+patterns",
      "value": [
        "charkop",
        "kandivali",
        "kandivali west"
      ]
    },
    "location.primary_location": {
      "confidence": 80,
      "source": "dictionary+patterns",
      "value": "charkop"
    },
    "location.railway_line": {
      "confidence": 85,
      "source": "dictionary",
      "value": "western"
    },
    "metadata.contact_numbers": {
      "confidence": 95,
      "source": "regex+llm",
      "value": [
        "9820067788"
      ]
    },
    "metadata.contact_people": {
      "confidence": 0,
      "source": "llm+cleanup",
      "value": []
    },
    "metadata.message_title": {
      "confidence": 75,
      "source": "llm+rules",
      "value": "Flat"
    },
    "parking.parking_count": {
      "confidence": 0,
      "source": "regex",
      "value": null
    },
    "parking.parking_type": {
      "confidence": 0,
      "source": "keyword",
      "value": null
    },
    "pricing.deposit_price": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.price": {
      "confidence": 85,
      "source": "regex+rules",
      "value": 11000000
    },
    "pricing.price_max": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.price_min": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.rent_price": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "property.all_detected_subtypes": {
      "confidence": 75,
      "source": "keyword+llm",
      "value": [
        "apartment"
      ]
    },
    "property.property_subtype": {
      "confidence": 80,
      "source": "keyword+llm",
      "value": "apartment"
    },
    "summary.bhk": {
      "confidence": 90,
      "source": "regex",
      "value": 1
    },
    "summary.request_type": {
      "confidence": 90,
      "source": "keyword+rules",
      "value": "requirement"
    }
  },
  "location": {
    "locations": [
      "charkop",
      "kandivali",
      "kandivali west"
    ],
    "primary_location": "charkop",
    "railway_line": "western"
  },
  "metadata": {
    "contact_numbers": [
      "9820067788"
    ],
    "contact_people": [],
    "message_title": "Flat",
    "metadata_summary": {
      "has_contact": true,
      "total_contacts": 0,
      "total_numbers": 1
    }
  },
  "parking": {
    "parking_count": null,
    "parking_type": null
  },
  "pricing": {
    "deposit_price": null,
    "price": 11000000,
    "price_max": null,
    "price_min": null,
    "rent_price": null
  },
  "property": {
    "all_detected_subtypes": [
      "apartment"
    ],
    "property_subtype": "apartment"
  },
  "summary": {
    "bhk": 1,
    "request_type": "requirement"
  }
}
```

## 7. single_property_Dataset/requirements/02.md

- Sample accuracy: 71.43% (5/7)

### Original message

```text
Need 2 bhk flat on rent
Budget 45000
Near metro preferred
Family client

Contact urgently
```

### Model response

```json
{
  "amenities": [
    "air conditioning"
  ],
  "attributes": {
    "facing": null,
    "furnishing": null
  },
  "extraction_meta": {
    "amenities": {
      "confidence": 75,
      "source": "regex+llm",
      "value": [
        "air conditioning"
      ]
    },
    "attributes.facing": {
      "confidence": 0,
      "source": "keyword",
      "value": null
    },
    "attributes.furnishing": {
      "confidence": 0,
      "source": "keyword+scoring",
      "value": null
    },
    "location.locations": {
      "confidence": 80,
      "source": "dictionary+patterns",
      "value": [
        "near metro preferred family client"
      ]
    },
    "location.primary_location": {
      "confidence": 80,
      "source": "dictionary+patterns",
      "value": "near metro preferred family client"
    },
    "location.railway_line": {
      "confidence": 0,
      "source": "dictionary",
      "value": null
    },
    "metadata.contact_numbers": {
      "confidence": 0,
      "source": "regex+llm",
      "value": []
    },
    "metadata.contact_people": {
      "confidence": 0,
      "source": "llm+cleanup",
      "value": []
    },
    "metadata.message_title": {
      "confidence": 75,
      "source": "llm+rules",
      "value": "Flat"
    },
    "parking.parking_count": {
      "confidence": 0,
      "source": "regex",
      "value": null
    },
    "parking.parking_type": {
      "confidence": 0,
      "source": "keyword",
      "value": null
    },
    "pricing.deposit_price": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.price": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.price_max": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.price_min": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.rent_price": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "property.all_detected_subtypes": {
      "confidence": 75,
      "source": "keyword+llm",
      "value": [
        "apartment"
      ]
    },
    "property.property_subtype": {
      "confidence": 80,
      "source": "keyword+llm",
      "value": "apartment"
    },
    "summary.bhk": {
      "confidence": 90,
      "source": "regex",
      "value": 2
    },
    "summary.request_type": {
      "confidence": 90,
      "source": "keyword+rules",
      "value": "requirement"
    }
  },
  "location": {
    "locations": [
      "near metro preferred family client"
    ],
    "primary_location": "near metro preferred family client",
    "railway_line": null
  },
  "metadata": {
    "contact_numbers": [],
    "contact_people": [],
    "message_title": "Flat",
    "metadata_summary": {
      "has_contact": false,
      "total_contacts": 0,
      "total_numbers": 0
    }
  },
  "parking": {
    "parking_count": null,
    "parking_type": null
  },
  "pricing": {
    "deposit_price": null,
    "price": null,
    "price_max": null,
    "price_min": null,
    "rent_price": null
  },
  "property": {
    "all_detected_subtypes": [
      "apartment"
    ],
    "property_subtype": "apartment"
  },
  "summary": {
    "bhk": 2,
    "request_type": "requirement"
  }
}
```

## 8. single_property_Dataset/requirements/03.md

- Sample accuracy: 60.00% (6/10)

### Original message

```text
Urgent Requirement

3 bhk furnished flat required in Borivali West
Budget 2.5 cr
Immediate closing

Broker pls contact
```

### Model response

```json
{
  "amenities": [
    "air conditioning"
  ],
  "attributes": {
    "facing": null,
    "furnishing": "fully_furnished"
  },
  "extraction_meta": {
    "amenities": {
      "confidence": 75,
      "source": "regex+llm",
      "value": [
        "air conditioning"
      ]
    },
    "attributes.facing": {
      "confidence": 0,
      "source": "keyword",
      "value": null
    },
    "attributes.furnishing": {
      "confidence": 80,
      "source": "keyword+scoring",
      "value": "fully_furnished"
    },
    "location.locations": {
      "confidence": 80,
      "source": "dictionary+patterns",
      "value": [
        "borivali",
        "borivali west"
      ]
    },
    "location.primary_location": {
      "confidence": 80,
      "source": "dictionary+patterns",
      "value": "borivali"
    },
    "location.railway_line": {
      "confidence": 85,
      "source": "dictionary",
      "value": "western"
    },
    "metadata.contact_numbers": {
      "confidence": 0,
      "source": "regex+llm",
      "value": []
    },
    "metadata.contact_people": {
      "confidence": 0,
      "source": "llm+cleanup",
      "value": []
    },
    "metadata.message_title": {
      "confidence": 75,
      "source": "llm+rules",
      "value": "Flat"
    },
    "parking.parking_count": {
      "confidence": 0,
      "source": "regex",
      "value": null
    },
    "parking.parking_type": {
      "confidence": 0,
      "source": "keyword",
      "value": null
    },
    "pricing.deposit_price": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.price": {
      "confidence": 85,
      "source": "regex+rules",
      "value": 25000000
    },
    "pricing.price_max": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.price_min": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.rent_price": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "property.all_detected_subtypes": {
      "confidence": 75,
      "source": "keyword+llm",
      "value": [
        "apartment"
      ]
    },
    "property.property_subtype": {
      "confidence": 80,
      "source": "keyword+llm",
      "value": "apartment"
    },
    "summary.bhk": {
      "confidence": 90,
      "source": "regex",
      "value": 3
    },
    "summary.request_type": {
      "confidence": 90,
      "source": "keyword+rules",
      "value": "requirement"
    }
  },
  "location": {
    "locations": [
      "borivali",
      "borivali west"
    ],
    "primary_location": "borivali",
    "railway_line": "western"
  },
  "metadata": {
    "contact_numbers": [],
    "contact_people": [],
    "message_title": "Flat",
    "metadata_summary": {
      "has_contact": false,
      "total_contacts": 0,
      "total_numbers": 0
    }
  },
  "parking": {
    "parking_count": null,
    "parking_type": null
  },
  "pricing": {
    "deposit_price": null,
    "price": 25000000,
    "price_max": null,
    "price_min": null,
    "rent_price": null
  },
  "property": {
    "all_detected_subtypes": [
      "apartment"
    ],
    "property_subtype": "apartment"
  },
  "summary": {
    "bhk": 3,
    "request_type": "requirement"
  }
}
```

## 9. single_property_Dataset/requirements/04.md

- Sample accuracy: 60.00% (3/5)

### Original message

```text
Requirement for investor client

Need 2 bhk flat for outright purchase
Budget upto 2 cr
Ready possession only
```

### Model response

```json
{
  "amenities": [],
  "attributes": {
    "facing": null,
    "furnishing": null
  },
  "extraction_meta": {
    "amenities": {
      "confidence": 0,
      "source": "regex+llm",
      "value": []
    },
    "attributes.facing": {
      "confidence": 0,
      "source": "keyword",
      "value": null
    },
    "attributes.furnishing": {
      "confidence": 0,
      "source": "keyword+scoring",
      "value": null
    },
    "location.locations": {
      "confidence": 0,
      "source": "dictionary+patterns",
      "value": []
    },
    "location.primary_location": {
      "confidence": 0,
      "source": "dictionary+patterns",
      "value": null
    },
    "location.railway_line": {
      "confidence": 0,
      "source": "dictionary",
      "value": null
    },
    "metadata.contact_numbers": {
      "confidence": 0,
      "source": "regex+llm",
      "value": []
    },
    "metadata.contact_people": {
      "confidence": 0,
      "source": "llm+cleanup",
      "value": []
    },
    "metadata.message_title": {
      "confidence": 75,
      "source": "llm+rules",
      "value": "Flat"
    },
    "parking.parking_count": {
      "confidence": 0,
      "source": "regex",
      "value": null
    },
    "parking.parking_type": {
      "confidence": 0,
      "source": "keyword",
      "value": null
    },
    "pricing.deposit_price": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.price": {
      "confidence": 85,
      "source": "regex+rules",
      "value": 20000000
    },
    "pricing.price_max": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.price_min": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.rent_price": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "property.all_detected_subtypes": {
      "confidence": 75,
      "source": "keyword+llm",
      "value": [
        "apartment"
      ]
    },
    "property.property_subtype": {
      "confidence": 80,
      "source": "keyword+llm",
      "value": "apartment"
    },
    "summary.bhk": {
      "confidence": 90,
      "source": "regex",
      "value": 2
    },
    "summary.request_type": {
      "confidence": 90,
      "source": "keyword+rules",
      "value": "requirement"
    }
  },
  "location": {
    "locations": [],
    "primary_location": null,
    "railway_line": null
  },
  "metadata": {
    "contact_numbers": [],
    "contact_people": [],
    "message_title": "Flat",
    "metadata_summary": {
      "has_contact": false,
      "total_contacts": 0,
      "total_numbers": 0
    }
  },
  "parking": {
    "parking_count": null,
    "parking_type": null
  },
  "pricing": {
    "deposit_price": null,
    "price": 20000000,
    "price_max": null,
    "price_min": null,
    "rent_price": null
  },
  "property": {
    "all_detected_subtypes": [
      "apartment"
    ],
    "property_subtype": "apartment"
  },
  "summary": {
    "bhk": 2,
    "request_type": "requirement"
  }
}
```

## 10. single_property_Dataset/requirements/049.md

- Sample accuracy: 85.71% (6/7)

### Original message

```text
Need commercial office on rent
300 carpet minimum
Near link road preferred

Immediate possession required
```

### Model response

```json
{
  "amenities": [],
  "attributes": {
    "facing": null,
    "furnishing": null
  },
  "extraction_meta": {
    "amenities": {
      "confidence": 0,
      "source": "regex+llm",
      "value": []
    },
    "attributes.facing": {
      "confidence": 0,
      "source": "keyword",
      "value": null
    },
    "attributes.furnishing": {
      "confidence": 0,
      "source": "keyword+scoring",
      "value": null
    },
    "location.locations": {
      "confidence": 80,
      "source": "dictionary+patterns",
      "value": [
        "near link road preferred immediate",
        "link road"
      ]
    },
    "location.primary_location": {
      "confidence": 80,
      "source": "dictionary+patterns",
      "value": "near link road preferred immediate"
    },
    "location.railway_line": {
      "confidence": 0,
      "source": "dictionary",
      "value": null
    },
    "metadata.contact_numbers": {
      "confidence": 0,
      "source": "regex+llm",
      "value": []
    },
    "metadata.contact_people": {
      "confidence": 0,
      "source": "llm+cleanup",
      "value": []
    },
    "metadata.message_title": {
      "confidence": 75,
      "source": "llm+rules",
      "value": "Flat"
    },
    "parking.parking_count": {
      "confidence": 0,
      "source": "regex",
      "value": null
    },
    "parking.parking_type": {
      "confidence": 0,
      "source": "keyword",
      "value": null
    },
    "pricing.deposit_price": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.price": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.price_max": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.price_min": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.rent_price": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "property.all_detected_subtypes": {
      "confidence": 75,
      "source": "keyword+llm",
      "value": [
        "commercial_space",
        "office"
      ]
    },
    "property.property_subtype": {
      "confidence": 80,
      "source": "keyword+llm",
      "value": "office"
    },
    "summary.bhk": {
      "confidence": 0,
      "source": "regex",
      "value": null
    },
    "summary.request_type": {
      "confidence": 90,
      "source": "keyword+rules",
      "value": "requirement"
    }
  },
  "location": {
    "locations": [
      "near link road preferred immediate",
      "link road"
    ],
    "primary_location": "near link road preferred immediate",
    "railway_line": null
  },
  "metadata": {
    "contact_numbers": [],
    "contact_people": [],
    "message_title": "Flat",
    "metadata_summary": {
      "has_contact": false,
      "total_contacts": 0,
      "total_numbers": 0
    }
  },
  "parking": {
    "parking_count": null,
    "parking_type": null
  },
  "pricing": {
    "deposit_price": null,
    "price": null,
    "price_max": null,
    "price_min": null,
    "rent_price": null
  },
  "property": {
    "all_detected_subtypes": [
      "commercial_space",
      "office"
    ],
    "property_subtype": "office"
  },
  "summary": {
    "bhk": null,
    "request_type": "requirement"
  }
}
```

## 11. single_property_Dataset/requirements/06.md

- Sample accuracy: 100.00% (4/4)

### Original message

```text
Client Requirement

Need 4 bhk bungalow in Lonavala
Budget flexible
Ready to move preferred
```

### Model response

```json
{
  "amenities": [],
  "attributes": {
    "facing": null,
    "furnishing": null
  },
  "extraction_meta": {
    "amenities": {
      "confidence": 0,
      "source": "regex+llm",
      "value": []
    },
    "attributes.facing": {
      "confidence": 0,
      "source": "keyword",
      "value": null
    },
    "attributes.furnishing": {
      "confidence": 0,
      "source": "keyword+scoring",
      "value": null
    },
    "location.locations": {
      "confidence": 0,
      "source": "dictionary+patterns",
      "value": []
    },
    "location.primary_location": {
      "confidence": 0,
      "source": "dictionary+patterns",
      "value": null
    },
    "location.railway_line": {
      "confidence": 0,
      "source": "dictionary",
      "value": null
    },
    "metadata.contact_numbers": {
      "confidence": 0,
      "source": "regex+llm",
      "value": []
    },
    "metadata.contact_people": {
      "confidence": 0,
      "source": "llm+cleanup",
      "value": []
    },
    "metadata.message_title": {
      "confidence": 75,
      "source": "llm+rules",
      "value": "Flat"
    },
    "parking.parking_count": {
      "confidence": 0,
      "source": "regex",
      "value": null
    },
    "parking.parking_type": {
      "confidence": 0,
      "source": "keyword",
      "value": null
    },
    "pricing.deposit_price": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.price": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.price_max": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.price_min": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.rent_price": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "property.all_detected_subtypes": {
      "confidence": 75,
      "source": "keyword+llm",
      "value": [
        "bungalow"
      ]
    },
    "property.property_subtype": {
      "confidence": 80,
      "source": "keyword+llm",
      "value": "bungalow"
    },
    "summary.bhk": {
      "confidence": 90,
      "source": "regex",
      "value": 4
    },
    "summary.request_type": {
      "confidence": 90,
      "source": "keyword+rules",
      "value": "requirement"
    }
  },
  "location": {
    "locations": [],
    "primary_location": null,
    "railway_line": null
  },
  "metadata": {
    "contact_numbers": [],
    "contact_people": [],
    "message_title": "Flat",
    "metadata_summary": {
      "has_contact": false,
      "total_contacts": 0,
      "total_numbers": 0
    }
  },
  "parking": {
    "parking_count": null,
    "parking_type": null
  },
  "pricing": {
    "deposit_price": null,
    "price": null,
    "price_max": null,
    "price_min": null,
    "rent_price": null
  },
  "property": {
    "all_detected_subtypes": [
      "bungalow"
    ],
    "property_subtype": "bungalow"
  },
  "summary": {
    "bhk": 4,
    "request_type": "requirement"
  }
}
```

## 12. single_property_Dataset/sale/01.md

- Sample accuracy: 71.43% (5/7)

### Original message

```text
1 BHK
Kanakya park
With car parking
Asking 1.05 Cr
```

### Model response

```json
{
  "amenities": [
    "parking"
  ],
  "attributes": {
    "facing": null,
    "furnishing": null
  },
  "extraction_meta": {
    "amenities": {
      "confidence": 75,
      "source": "regex+llm",
      "value": [
        "parking"
      ]
    },
    "attributes.facing": {
      "confidence": 0,
      "source": "keyword",
      "value": null
    },
    "attributes.furnishing": {
      "confidence": 0,
      "source": "keyword+scoring",
      "value": null
    },
    "location.locations": {
      "confidence": 0,
      "source": "dictionary+patterns",
      "value": []
    },
    "location.primary_location": {
      "confidence": 0,
      "source": "dictionary+patterns",
      "value": null
    },
    "location.railway_line": {
      "confidence": 0,
      "source": "dictionary",
      "value": null
    },
    "metadata.contact_numbers": {
      "confidence": 0,
      "source": "regex+llm",
      "value": []
    },
    "metadata.contact_people": {
      "confidence": 0,
      "source": "llm+cleanup",
      "value": []
    },
    "metadata.message_title": {
      "confidence": 75,
      "source": "llm+rules",
      "value": "Flat"
    },
    "parking.parking_count": {
      "confidence": 80,
      "source": "regex",
      "value": 1
    },
    "parking.parking_type": {
      "confidence": 80,
      "source": "keyword",
      "value": "car"
    },
    "pricing.deposit_price": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.price": {
      "confidence": 85,
      "source": "regex+rules",
      "value": 10500000
    },
    "pricing.price_max": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.price_min": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.rent_price": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "property.all_detected_subtypes": {
      "confidence": 0,
      "source": "keyword+llm",
      "value": []
    },
    "property.property_subtype": {
      "confidence": 80,
      "source": "keyword+llm",
      "value": "apartment"
    },
    "summary.bhk": {
      "confidence": 90,
      "source": "regex",
      "value": 1
    },
    "summary.request_type": {
      "confidence": 90,
      "source": "keyword+rules",
      "value": "sale"
    }
  },
  "location": {
    "locations": [],
    "primary_location": null,
    "railway_line": null
  },
  "metadata": {
    "contact_numbers": [],
    "contact_people": [],
    "message_title": "Flat",
    "metadata_summary": {
      "has_contact": false,
      "total_contacts": 0,
      "total_numbers": 0
    }
  },
  "parking": {
    "parking_count": 1,
    "parking_type": "car"
  },
  "pricing": {
    "deposit_price": null,
    "price": 10500000,
    "price_max": null,
    "price_min": null,
    "rent_price": null
  },
  "property": {
    "all_detected_subtypes": [],
    "property_subtype": "apartment"
  },
  "summary": {
    "bhk": 1,
    "request_type": "sale"
  }
}
```

## 13. single_property_Dataset/sale/02.md

- Sample accuracy: 55.56% (5/9)

### Original message

```text
2 BHK
Radha residency
With car parking
Furnished flat
Asking 2.85 CR
```

### Model response

```json
{
  "amenities": [
    "parking"
  ],
  "attributes": {
    "facing": null,
    "furnishing": "fully_furnished"
  },
  "extraction_meta": {
    "amenities": {
      "confidence": 75,
      "source": "regex+llm",
      "value": [
        "parking"
      ]
    },
    "attributes.facing": {
      "confidence": 0,
      "source": "keyword",
      "value": null
    },
    "attributes.furnishing": {
      "confidence": 80,
      "source": "keyword+scoring",
      "value": "fully_furnished"
    },
    "location.locations": {
      "confidence": 0,
      "source": "dictionary+patterns",
      "value": []
    },
    "location.primary_location": {
      "confidence": 0,
      "source": "dictionary+patterns",
      "value": null
    },
    "location.railway_line": {
      "confidence": 0,
      "source": "dictionary",
      "value": null
    },
    "metadata.contact_numbers": {
      "confidence": 0,
      "source": "regex+llm",
      "value": []
    },
    "metadata.contact_people": {
      "confidence": 0,
      "source": "llm+cleanup",
      "value": []
    },
    "metadata.message_title": {
      "confidence": 75,
      "source": "llm+rules",
      "value": "Flat"
    },
    "parking.parking_count": {
      "confidence": 80,
      "source": "regex",
      "value": 1
    },
    "parking.parking_type": {
      "confidence": 80,
      "source": "keyword",
      "value": "car"
    },
    "pricing.deposit_price": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.price": {
      "confidence": 85,
      "source": "regex+rules",
      "value": 28500000
    },
    "pricing.price_max": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.price_min": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.rent_price": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "property.all_detected_subtypes": {
      "confidence": 75,
      "source": "keyword+llm",
      "value": [
        "apartment"
      ]
    },
    "property.property_subtype": {
      "confidence": 80,
      "source": "keyword+llm",
      "value": "apartment"
    },
    "summary.bhk": {
      "confidence": 90,
      "source": "regex",
      "value": 2
    },
    "summary.request_type": {
      "confidence": 90,
      "source": "keyword+rules",
      "value": "sale"
    }
  },
  "location": {
    "locations": [],
    "primary_location": null,
    "railway_line": null
  },
  "metadata": {
    "contact_numbers": [],
    "contact_people": [],
    "message_title": "Flat",
    "metadata_summary": {
      "has_contact": false,
      "total_contacts": 0,
      "total_numbers": 0
    }
  },
  "parking": {
    "parking_count": 1,
    "parking_type": "car"
  },
  "pricing": {
    "deposit_price": null,
    "price": 28500000,
    "price_max": null,
    "price_min": null,
    "rent_price": null
  },
  "property": {
    "all_detected_subtypes": [
      "apartment"
    ],
    "property_subtype": "apartment"
  },
  "summary": {
    "bhk": 2,
    "request_type": "sale"
  }
}
```

## 14. single_property_Dataset/sale/03.md

- Sample accuracy: 71.43% (5/7)

### Original message

```text
3 BHK
Oberoi sky City
Middle floor
2 car parking
Asking 4.7Cr
```

### Model response

```json
{
  "amenities": [
    "parking"
  ],
  "attributes": {
    "facing": null,
    "furnishing": null
  },
  "extraction_meta": {
    "amenities": {
      "confidence": 75,
      "source": "regex+llm",
      "value": [
        "parking"
      ]
    },
    "attributes.facing": {
      "confidence": 0,
      "source": "keyword",
      "value": null
    },
    "attributes.furnishing": {
      "confidence": 0,
      "source": "keyword+scoring",
      "value": null
    },
    "location.locations": {
      "confidence": 0,
      "source": "dictionary+patterns",
      "value": []
    },
    "location.primary_location": {
      "confidence": 0,
      "source": "dictionary+patterns",
      "value": null
    },
    "location.railway_line": {
      "confidence": 0,
      "source": "dictionary",
      "value": null
    },
    "metadata.contact_numbers": {
      "confidence": 0,
      "source": "regex+llm",
      "value": []
    },
    "metadata.contact_people": {
      "confidence": 0,
      "source": "llm+cleanup",
      "value": []
    },
    "metadata.message_title": {
      "confidence": 75,
      "source": "llm+rules",
      "value": "Flat"
    },
    "parking.parking_count": {
      "confidence": 80,
      "source": "regex",
      "value": 2
    },
    "parking.parking_type": {
      "confidence": 80,
      "source": "keyword",
      "value": "car"
    },
    "pricing.deposit_price": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.price": {
      "confidence": 85,
      "source": "regex+rules",
      "value": 47000000
    },
    "pricing.price_max": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.price_min": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.rent_price": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "property.all_detected_subtypes": {
      "confidence": 0,
      "source": "keyword+llm",
      "value": []
    },
    "property.property_subtype": {
      "confidence": 80,
      "source": "keyword+llm",
      "value": "apartment"
    },
    "summary.bhk": {
      "confidence": 90,
      "source": "regex",
      "value": 3
    },
    "summary.request_type": {
      "confidence": 90,
      "source": "keyword+rules",
      "value": "sale"
    }
  },
  "location": {
    "locations": [],
    "primary_location": null,
    "railway_line": null
  },
  "metadata": {
    "contact_numbers": [],
    "contact_people": [],
    "message_title": "Flat",
    "metadata_summary": {
      "has_contact": false,
      "total_contacts": 0,
      "total_numbers": 0
    }
  },
  "parking": {
    "parking_count": 2,
    "parking_type": "car"
  },
  "pricing": {
    "deposit_price": null,
    "price": 47000000,
    "price_max": null,
    "price_min": null,
    "rent_price": null
  },
  "property": {
    "all_detected_subtypes": [],
    "property_subtype": "apartment"
  },
  "summary": {
    "bhk": 3,
    "request_type": "sale"
  }
}
```

## 15. single_property_Dataset/sale/04.md

- Sample accuracy: 66.67% (4/6)

### Original message

```text
🔹 3 BHK | 1036 Sqft | 22nd Floor
💰 ₹3.78 Cr
✅ OC June 2025 | Immediate Possession | 1 Parking
```

### Model response

```json
{
  "amenities": [
    "parking"
  ],
  "attributes": {
    "facing": null,
    "furnishing": null
  },
  "extraction_meta": {
    "amenities": {
      "confidence": 75,
      "source": "regex+llm",
      "value": [
        "parking"
      ]
    },
    "attributes.facing": {
      "confidence": 0,
      "source": "keyword",
      "value": null
    },
    "attributes.furnishing": {
      "confidence": 0,
      "source": "keyword+scoring",
      "value": null
    },
    "location.locations": {
      "confidence": 0,
      "source": "dictionary+patterns",
      "value": []
    },
    "location.primary_location": {
      "confidence": 0,
      "source": "dictionary+patterns",
      "value": null
    },
    "location.railway_line": {
      "confidence": 0,
      "source": "dictionary",
      "value": null
    },
    "metadata.contact_numbers": {
      "confidence": 0,
      "source": "regex+llm",
      "value": []
    },
    "metadata.contact_people": {
      "confidence": 0,
      "source": "llm+cleanup",
      "value": []
    },
    "metadata.message_title": {
      "confidence": 75,
      "source": "llm+rules",
      "value": "Flat"
    },
    "parking.parking_count": {
      "confidence": 80,
      "source": "regex",
      "value": 1
    },
    "parking.parking_type": {
      "confidence": 0,
      "source": "keyword",
      "value": null
    },
    "pricing.deposit_price": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.price": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.price_max": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.price_min": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.rent_price": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "property.all_detected_subtypes": {
      "confidence": 0,
      "source": "keyword+llm",
      "value": []
    },
    "property.property_subtype": {
      "confidence": 80,
      "source": "keyword+llm",
      "value": "apartment"
    },
    "summary.bhk": {
      "confidence": 90,
      "source": "regex",
      "value": 3
    },
    "summary.request_type": {
      "confidence": 90,
      "source": "keyword+rules",
      "value": "sale"
    }
  },
  "location": {
    "locations": [],
    "primary_location": null,
    "railway_line": null
  },
  "metadata": {
    "contact_numbers": [],
    "contact_people": [],
    "message_title": "Flat",
    "metadata_summary": {
      "has_contact": false,
      "total_contacts": 0,
      "total_numbers": 0
    }
  },
  "parking": {
    "parking_count": 1,
    "parking_type": null
  },
  "pricing": {
    "deposit_price": null,
    "price": 37800000,
    "price_max": null,
    "price_min": null,
    "rent_price": null
  },
  "property": {
    "all_detected_subtypes": [],
    "property_subtype": "apartment"
  },
  "summary": {
    "bhk": 3,
    "request_type": "sale"
  }
}
```

## 16. single_property_Dataset/sale/06.md

- Sample accuracy: 81.82% (9/11)

### Original message

```text
2 BHK
Rizvi Cedar Tower
Malad East
Semi furnished
With car parking
Asking 1.62 Cr
```

### Model response

```json
{
  "amenities": [
    "parking"
  ],
  "attributes": {
    "facing": null,
    "furnishing": "semi_furnished"
  },
  "extraction_meta": {
    "amenities": {
      "confidence": 75,
      "source": "regex+llm",
      "value": [
        "parking"
      ]
    },
    "attributes.facing": {
      "confidence": 0,
      "source": "keyword",
      "value": null
    },
    "attributes.furnishing": {
      "confidence": 80,
      "source": "keyword+scoring",
      "value": "semi_furnished"
    },
    "location.locations": {
      "confidence": 80,
      "source": "dictionary+patterns",
      "value": [
        "2 bhk rizvi cedar tower",
        "malad",
        "malad east"
      ]
    },
    "location.primary_location": {
      "confidence": 80,
      "source": "dictionary+patterns",
      "value": "2 bhk rizvi cedar tower"
    },
    "location.railway_line": {
      "confidence": 85,
      "source": "dictionary",
      "value": "western"
    },
    "metadata.contact_numbers": {
      "confidence": 0,
      "source": "regex+llm",
      "value": []
    },
    "metadata.contact_people": {
      "confidence": 0,
      "source": "llm+cleanup",
      "value": []
    },
    "metadata.message_title": {
      "confidence": 75,
      "source": "llm+rules",
      "value": "Flat"
    },
    "parking.parking_count": {
      "confidence": 80,
      "source": "regex",
      "value": 1
    },
    "parking.parking_type": {
      "confidence": 80,
      "source": "keyword",
      "value": "car"
    },
    "pricing.deposit_price": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.price": {
      "confidence": 85,
      "source": "regex+rules",
      "value": 16200000
    },
    "pricing.price_max": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.price_min": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "pricing.rent_price": {
      "confidence": 0,
      "source": "regex+rules",
      "value": null
    },
    "property.all_detected_subtypes": {
      "confidence": 0,
      "source": "keyword+llm",
      "value": []
    },
    "property.property_subtype": {
      "confidence": 80,
      "source": "keyword+llm",
      "value": "apartment"
    },
    "summary.bhk": {
      "confidence": 90,
      "source": "regex",
      "value": 2
    },
    "summary.request_type": {
      "confidence": 90,
      "source": "keyword+rules",
      "value": "sale"
    }
  },
  "location": {
    "locations": [
      "Rizvi Cedar Tower",
      "Malad East"
    ],
    "primary_location": "Malad East",
    "railway_line": "western"
  },
  "metadata": {
    "contact_numbers": [],
    "contact_people": [],
    "message_title": "Flat",
    "metadata_summary": {
      "has_contact": false,
      "total_contacts": 0,
      "total_numbers": 0
    }
  },
  "parking": {
    "parking_count": 1,
    "parking_type": "car"
  },
  "pricing": {
    "deposit_price": null,
    "price": 1620000,
    "price_max": null,
    "price_min": null,
    "rent_price": null
  },
  "property": {
    "all_detected_subtypes": [],
    "property_subtype": "apartment"
  },
  "summary": {
    "bhk": 2,
    "request_type": "sale"
  }
}
```
